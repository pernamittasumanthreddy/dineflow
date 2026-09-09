from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.orders.models import Order, OrderItem, OrderItemAddon, OrderStatusHistory, OrderTax
from apps.kitchen.models import KitchenOrder, KitchenOrderItem, KitchenStation
from apps.payments.models import Payment, PaymentMethod, PaymentTransaction
from apps.billing.models import Invoice
from apps.tables.models import RestaurantTable
from apps.audit.models import AuditLog
from services.inventory_service import InventoryService
from services.billing_service import BillingService


class OrderService:
    @classmethod
    @transaction.atomic
    def place_order(
        cls,
        branch,
        order_type: str,
        items_data: list,
        table=None,
        waiter=None,
        customer=None,
        notes: str = '',
        user=None
    ) -> Order:
        """
        Creates an Order with OrderItems, recalculates totals, updates Table status if Dine-in,
        generates KOT (Kitchen Order Ticket), and records initial OrderStatusHistory.
        """
        restaurant = branch.restaurant
        order_count = Order.objects.filter(branch=branch).count() + 1
        order_number = f"ORD-{branch.code}-{timezone.now().strftime('%Y%m%d')}-{order_count:04d}"

        order = Order.objects.create(
            restaurant=restaurant,
            branch=branch,
            order_number=order_number,
            order_type=order_type,
            table=table,
            waiter=waiter,
            customer=customer,
            status='PLACED',
            placed_at=timezone.now(),
        )

        subtotal = Decimal('0.00')
        total_items_count = 0

        for item_info in items_data:
            menu_item = item_info['menu_item']
            variant = item_info.get('variant')
            quantity = item_info.get('quantity', 1)
            unit_price = variant.price if variant else menu_item.base_price
            line_subtotal = (unit_price * Decimal(str(quantity))).quantize(Decimal('0.01'))
            discount_amount = item_info.get('discount_amount', Decimal('0.00'))
            taxable = max(Decimal('0.00'), line_subtotal - discount_amount)
            tax_amount = (taxable * Decimal('0.05')).quantize(Decimal('0.01'))
            total_price = taxable + tax_amount

            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                menu_variant=variant,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=line_subtotal,
                discount_amount=discount_amount,
                tax_amount=tax_amount,
                total_price=total_price,
                special_instructions=item_info.get('special_instructions', ''),
                status='RECEIVED'
            )

            # Addons
            for addon_info in item_info.get('addons', []):
                addon = addon_info['addon']
                addon_qty = addon_info.get('quantity', 1)
                addon_price = addon.price
                addon_total = addon_price * Decimal(str(addon_qty))
                OrderItemAddon.objects.create(
                    order_item=order_item,
                    addon=addon,
                    quantity=addon_qty,
                    unit_price=addon_price,
                    total_price=addon_total
                )
                subtotal += addon_total

            subtotal += line_subtotal
            total_items_count += quantity

        # 5% Restaurant GST (2.5% CGST + 2.5% SGST)
        tax_total = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
        final_amount = subtotal + tax_total

        order.total_item_count = total_items_count
        order.subtotal = subtotal
        order.tax_amount = tax_total
        order.final_amount = final_amount
        order.save()

        # Update Table status if Dine-in
        if table and order_type == 'DINE_IN':
            table.status = 'OCCUPIED'
            table.save(update_fields=['status', 'updated_at'])

        # Initial Status History
        OrderStatusHistory.objects.create(
            order=order,
            old_status='DRAFT',
            new_status='PLACED',
            changed_by=user,
            notes='Order placed successfully'
        )

        # Generate KOT
        cls.generate_kot_for_order(order, user)

        AuditLog.objects.create(
            action='CREATE',
            model_name='Order',
            object_id=str(order.id),
            object_repr=str(order),
            user=user,
            branch=branch,
            changes={'status': [None, 'PLACED'], 'final_amount': [None, str(final_amount)]}
        )

        return order

    @classmethod
    @transaction.atomic
    def generate_kot_for_order(cls, order: Order, user=None) -> KitchenOrder:
        """
        Creates a Kitchen Order Ticket (KOT) and items for the kitchen display system.
        """
        kot_count = KitchenOrder.objects.filter(branch=order.branch).count() + 1
        kot_number = f"KOT-{order.branch.code}-{timezone.now().strftime('%Y%m%d')}-{kot_count:04d}"

        # Station routing: default or first active station in branch
        station = KitchenStation.objects.filter(branch=order.branch, is_active=True).first()

        kot = KitchenOrder.objects.create(
            order=order,
            branch=order.branch,
            station=station,
            kot_number=kot_number,
            priority='NORMAL',
            status='RECEIVED',
            notes=f"KOT for Order #{order.order_number}"
        )

        for oi in order.items.all():
            KitchenOrderItem.objects.create(
                kitchen_order=kot,
                order_item=oi,
                quantity=oi.quantity,
                status='RECEIVED',
                notes=oi.special_instructions
            )

        return kot

    @classmethod
    @transaction.atomic
    def transition_order_status(cls, order: Order, new_status: str, user=None, notes: str = ''):
        """
        Transitions order lifecycle status with validations, inventory consumption, and audit trail.
        """
        old_status = order.status
        if old_status == new_status:
            return order

        # If transitioning to PREPARING or CONFIRMED, consume raw recipe BOM ingredients
        if new_status in ['PREPARING', 'CONFIRMED'] and old_status in ['PLACED', 'RECEIVED']:
            InventoryService.consume_recipe_ingredients_for_order(order, user)

        order.status = new_status
        if new_status == 'COMPLETED':
            order.closed_at = timezone.now()
            if order.table:
                order.table.status = 'CLEANING'
                order.table.save(update_fields=['status', 'updated_at'])

        order.save(update_fields=['status', 'closed_at', 'updated_at'])

        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=user,
            notes=notes
        )

        AuditLog.objects.create(
            action='UPDATE',
            model_name='Order',
            object_id=str(order.id),
            object_repr=str(order),
            user=user,
            branch=order.branch,
            changes={'status': [old_status, new_status]}
        )

        return order

    @classmethod
    @transaction.atomic
    def process_order_payment(
        cls,
        order: Order,
        payment_method_code: str,
        amount: Decimal,
        transaction_reference: str = '',
        user=None
    ) -> Payment:
        """
        Records payment for an order and its invoice, updating status to PAID and clearing table.
        """
        # Ensure invoice exists
        if not hasattr(order, 'invoice') or not order.invoice:
            invoice = BillingService.generate_invoice_for_order(order, user=user)
        else:
            invoice = order.invoice

        payment_method = PaymentMethod.objects.get(code=payment_method_code)

        payment = Payment.objects.create(
            invoice=invoice,
            order=order,
            branch=order.branch,
            payment_method=payment_method,
            amount=amount,
            transaction_reference=transaction_reference,
            status='SUCCESS',
            paid_at=timezone.now(),
            received_by=user,
        )

        PaymentTransaction.objects.create(
            payment=payment,
            transaction_type='PAYMENT',
            amount=amount,
            status='SUCCESS',
            metadata={'reference': transaction_reference, 'channel': payment_method.name}
        )

        # Update invoice status to PAID
        invoice.status = 'PAID'
        invoice.save(update_fields=['status', 'updated_at'])

        # Update order status to PAID
        cls.transition_order_status(order, 'PAID', user=user, notes=f"Paid ₹{amount} via {payment_method.name}")

        AuditLog.objects.create(
            action='PAYMENT',
            model_name='Payment',
            object_id=str(payment.id),
            object_repr=str(payment),
            user=user,
            branch=order.branch,
            changes={'amount': [None, str(amount)], 'method': [None, payment_method.name]}
        )

        return payment
