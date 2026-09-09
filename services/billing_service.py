from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.utils import timezone
from apps.billing.models import Invoice, InvoiceItem, InvoiceTax, InvoiceDiscount, InvoiceNumberSequence
from apps.orders.models import Order
from apps.audit.models import AuditLog


def get_current_fiscal_year(date_obj=None, start_month=4):
    """
    Returns the Indian fiscal year representation, e.g. '2026-27'
    for April 1, 2026 through March 31, 2027.
    """
    if date_obj is None:
        date_obj = timezone.now().date()
    elif hasattr(date_obj, 'date'):
        date_obj = date_obj.date()

    year = date_obj.year
    if date_obj.month >= start_month:
        next_year_suffix = str(year + 1)[-2:]
        return f"{year}-{next_year_suffix}"
    else:
        prev_year = year - 1
        curr_year_suffix = str(year)[-2:]
        return f"{prev_year}-{curr_year_suffix}"


class BillingService:
    @classmethod
    @transaction.atomic
    def generate_invoice_for_order(
        cls,
        order: Order,
        customer_name: str = '',
        customer_phone: str = '',
        customer_gstin: str = '',
        user=None,
        is_inter_state: bool = False
    ) -> Invoice:
        """
        Creates an Indian Tax Invoice for an order inside an atomic transaction.
        Uses row-level locking on InvoiceNumberSequence to prevent sequence duplication or race conditions.
        """
        # Ensure order is not already invoiced
        if hasattr(order, 'invoice') and order.invoice:
            return order.invoice

        branch = order.branch
        restaurant = order.restaurant
        settings = getattr(restaurant, 'settings', None)
        fiscal_year = get_current_fiscal_year(
            timezone.now(),
            start_month=settings.fiscal_year_start_month if settings else 4
        )
        prefix = settings.invoice_prefix if settings else 'INV'

        # Row-level pessimistic locking on sequence
        sequence_obj, _ = InvoiceNumberSequence.objects.select_for_update().get_or_create(
            branch=branch,
            fiscal_year=fiscal_year,
            prefix=prefix,
            defaults={'last_number': 0}
        )

        sequence_obj.last_number += 1
        sequence_obj.save(update_fields=['last_number', 'updated_at'])

        # Form invoice number: INV/HYD01/2026-27/00001
        invoice_number = f"{prefix}/{branch.code}/{fiscal_year}/{sequence_obj.last_number:05d}"

        # Financial computations
        subtotal = Decimal('0.00')
        total_discount = Decimal('0.00')
        items_payload = []

        for item in order.items.select_related('menu_item', 'menu_variant').all():
            qty = item.quantity
            unit_price = item.unit_price
            line_subtotal = item.subtotal
            line_discount = item.discount_amount
            taxable_amount = line_subtotal - line_discount
            if taxable_amount < 0:
                taxable_amount = Decimal('0.00')

            # Standard restaurant food GST rate: 5% (2.5% CGST + 2.5% SGST or 5% IGST)
            gst_rate = Decimal('5.00')
            if is_inter_state:
                cgst_rate = Decimal('0.00')
                sgst_rate = Decimal('0.00')
                cgst_amount = Decimal('0.00')
                sgst_amount = Decimal('0.00')
            else:
                cgst_rate = Decimal('2.50')
                sgst_rate = Decimal('2.50')
                cgst_amount = (taxable_amount * cgst_rate / Decimal('100.0')).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
                sgst_amount = (taxable_amount * sgst_rate / Decimal('100.0')).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )

            total_line_amount = taxable_amount + cgst_amount + sgst_amount

            subtotal += line_subtotal
            total_discount += line_discount

            items_payload.append({
                'item_name': item.menu_item.name,
                'hsn_sac_code': item.menu_item.hsn_code or '996331',
                'quantity': qty,
                'unit_price': unit_price,
                'discount_amount': line_discount,
                'taxable_amount': taxable_amount,
                'gst_rate': gst_rate,
                'cgst_rate': cgst_rate,
                'sgst_rate': sgst_rate,
                'cgst_amount': cgst_amount,
                'sgst_amount': sgst_amount,
                'total_amount': total_line_amount,
            })

        taxable_total = subtotal - total_discount
        if is_inter_state:
            cgst_total = Decimal('0.00')
            sgst_total = Decimal('0.00')
            igst_total = (taxable_total * Decimal('0.05')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            cgst_total = (taxable_total * Decimal('0.025')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            sgst_total = (taxable_total * Decimal('0.025')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            igst_total = Decimal('0.00')

        service_charge = order.service_charge or Decimal('0.00')
        raw_total = taxable_total + cgst_total + sgst_total + igst_total + service_charge
        rounded_total = raw_total.quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
        round_off = rounded_total - raw_total

        # Indian B2C UPI dynamic QR payload
        upi_id = branch.email or 'pay@dineflow'
        qr_code_data = (
            f"upi://pay?pa={upi_id}&pn={restaurant.name}&am={rounded_total:.2f}&cu=INR"
            f"&tr={invoice_number}&tn=Bill {invoice_number}"
        )

        customer_name_resolved = customer_name or (order.customer.name if order.customer else 'Guest Diner')
        customer_phone_resolved = customer_phone or (order.customer.phone if order.customer else '')

        # Create Invoice Header
        invoice = Invoice.objects.create(
            order=order,
            restaurant=restaurant,
            branch=branch,
            invoice_number=invoice_number,
            fiscal_year=fiscal_year,
            customer_name=customer_name_resolved,
            customer_phone=customer_phone_resolved,
            customer_gstin=customer_gstin,
            subtotal=subtotal,
            total_discount=total_discount,
            taxable_amount=taxable_total,
            cgst_amount=cgst_total,
            sgst_amount=sgst_total,
            igst_amount=igst_total,
            service_charge=service_charge,
            round_off=round_off,
            grand_total=rounded_total,
            status='ISSUED',
            qr_code_data=qr_code_data,
            created_by=user,
        )

        # Bulk create items
        invoice_items = [
            InvoiceItem(invoice=invoice, **item_data) for item_data in items_payload
        ]
        InvoiceItem.objects.bulk_create(invoice_items)

        # Create tax breakdowns
        if not is_inter_state:
            InvoiceTax.objects.create(
                invoice=invoice,
                tax_category_name='Food & Beverage GST 5%',
                component_name='CGST',
                rate_percent=Decimal('2.50'),
                taxable_amount=taxable_total,
                tax_amount=cgst_total,
            )
            InvoiceTax.objects.create(
                invoice=invoice,
                tax_category_name='Food & Beverage GST 5%',
                component_name='SGST',
                rate_percent=Decimal('2.50'),
                taxable_amount=taxable_total,
                tax_amount=sgst_total,
            )
        else:
            InvoiceTax.objects.create(
                invoice=invoice,
                tax_category_name='Food & Beverage GST 5%',
                component_name='IGST',
                rate_percent=Decimal('5.00'),
                taxable_amount=taxable_total,
                tax_amount=igst_total,
            )

        if total_discount > 0:
            InvoiceDiscount.objects.create(
                invoice=invoice,
                description='Special Promotional Discount',
                rate_or_flat=total_discount,
                discount_amount=total_discount,
            )

        # Update order status to BILLED
        order.status = 'BILLED'
        order.final_amount = rounded_total
        order.save(update_fields=['status', 'final_amount', 'updated_at'])

        # Audit logging
        AuditLog.objects.create(
            action='CREATE',
            model_name='Invoice',
            object_id=str(invoice.id),
            object_repr=str(invoice),
            user=user,
            branch=branch,
            changes={'grand_total': [None, str(rounded_total)], 'invoice_number': [None, invoice_number]}
        )

        return invoice
