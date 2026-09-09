"""Indian GST Invoice Generator, Thermal Printing, and Revenue Ledger Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.billing.models import Invoice, InvoiceItem
from apps.orders.models import Order, OrderStatus
from apps.restaurants.models import Restaurant
from apps.core.utils import calculate_gst_breakdown, round_inr
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('billing')
def generate_invoice_for_order_view(request, order_id):
    """Creates or refreshes the Indian GST tax invoice for an order."""
    order = get_object_or_404(Order, id=order_id)
    restaurant = Restaurant.objects.first()
    
    # Check if invoice already exists
    if hasattr(order, 'invoice'):
        return redirect('billing:detail', invoice_id=order.invoice.id)

    # Generate sequential invoice number: INV/YYYY-MM/XXXX
    now = timezone.now()
    year_month = now.strftime('%Y%m')
    inv_count = Invoice.objects.filter(created_at__year=now.year, created_at__month=now.month).count() + 1
    invoice_number = f"INV/{now.year}-{now.strftime('%m')}/{inv_count:04d}"

    # Calculate GST Breakdown
    subtotal = order.subtotal - order.discount_amount
    tax_rate = Decimal('5.00')  # Restaurant food standard GST
    gst_data = calculate_gst_breakdown(subtotal, tax_rate_percent=tax_rate, is_interstate=False)

    invoice = Invoice.objects.create(
        invoice_number=invoice_number,
        order=order,
        branch=order.branch,
        customer=order.customer,
        restaurant_name=restaurant.name if restaurant else "DineFlow Restaurant",
        restaurant_gstin=restaurant.gstin if restaurant else "36AAACN1234F1Z9",
        fssai_number=restaurant.fssai_number if restaurant else "13624014000189",
        branch_address=f"{order.branch.address}, {order.branch.city} - {order.branch.pincode}",
        taxable_subtotal=gst_data['subtotal'],
        discount_amount=order.discount_amount,
        cgst_amount=gst_data['cgst'],
        sgst_amount=gst_data['sgst'],
        igst_amount=gst_data['igst'],
        total_tax_amount=gst_data['total_tax'],
        grand_total=gst_data['grand_total'],
        is_paid=order.is_paid,
        cashier=request.user
    )

    # Create Itemized Billing Lines
    for item in order.items.all():
        line_tax = calculate_gst_breakdown(item.item_total, tax_rate_percent=item.menu_item.tax_rate_percent or Decimal('5.00'))
        InvoiceItem.objects.create(
            invoice=invoice,
            item_name=f"{item.menu_item.name} ({item.variant.name})" if item.variant else item.menu_item.name,
            sac_code='996331',
            quantity=item.quantity,
            unit_rate=item.unit_price,
            item_total=item.item_total,
            tax_rate_percent=item.menu_item.tax_rate_percent or Decimal('5.00'),
            cgst_amount=line_tax['cgst'],
            sgst_amount=line_tax['sgst']
        )

    messages.success(request, f"Invoice {invoice.invoice_number} generated successfully.")
    return redirect('billing:detail', invoice_id=invoice.id)

@login_required
def invoice_detail_view(request, invoice_id):
    """Detailed A4 Tax Invoice document."""
    invoice = get_object_or_404(Invoice.objects.select_related('order', 'customer', 'branch', 'cashier'), id=invoice_id)
    items = invoice.items.all()
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'items': items,
    })

@login_required
def thermal_receipt_view(request, invoice_id):
    """Compact 80mm/58mm thermal receipt layout for point-of-sale printers."""
    invoice = get_object_or_404(Invoice.objects.select_related('order', 'customer', 'branch', 'cashier'), id=invoice_id)
    items = invoice.items.all()
    return render(request, 'billing/thermal_receipt.html', {
        'invoice': invoice,
        'items': items,
    })

@login_required
@module_permission_required('billing')
def invoice_list_view(request):
    """Register of all generated tax invoices with revenue and tax filters."""
    branch = request.user.branch
    invoices = Invoice.objects.all().select_related('order', 'customer', 'branch', 'cashier')
    
    if branch:
        invoices = invoices.filter(branch=branch)
        
    date_filter = request.GET.get('date')
    search_q = request.GET.get('q')
    
    if date_filter:
        invoices = invoices.filter(created_at__date=date_filter)
    if search_q:
        invoices = invoices.filter(
            models.Q(invoice_number__icontains=search_q) |
            models.Q(customer__name__icontains=search_q) |
            models.Q(customer__phone__icontains=search_q)
        )
        
    invoices = invoices.order_by('-created_at')

    # Aggregates
    total_revenue = sum(inv.grand_total for inv in invoices)
    total_cgst = sum(inv.cgst_amount for inv in invoices)
    total_sgst = sum(inv.sgst_amount for inv in invoices)

    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices,
        'total_revenue': total_revenue,
        'total_cgst': total_cgst,
        'total_sgst': total_sgst,
        'date_filter': date_filter,
        'search_q': search_q,
    })
