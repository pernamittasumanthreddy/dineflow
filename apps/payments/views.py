"""Payment Settlement, Split Invoicing, and Local Simulation Views."""
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.orders.models import Order, OrderStatus
from apps.billing.models import Invoice
from apps.tables.models import TableStatus
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('payments')
def process_payment_view(request, order_id):
    """
    Simulated local checkout and payment settlement.
    Supports Cash, simulated UPI with QR string, and Card POS terminal swipe.
    """
    order = get_object_or_404(Order.objects.select_related('invoice', 'table', 'branch'), id=order_id)
    invoice = getattr(order, 'invoice', None)
    
    # Auto-generate invoice if not generated yet
    if not invoice:
        return redirect('billing:generate', order_id=order.id)

    if request.method == 'POST':
        method = request.POST.get('payment_method', PaymentMethod.CASH)
        amount_str = request.POST.get('amount', str(invoice.grand_total))
        amount = Decimal(amount_str)
        
        card_last4 = request.POST.get('card_last4', '')
        card_network = request.POST.get('card_network', 'RuPay')
        upi_vpa = request.POST.get('upi_vpa', '')
        
        # Generate internal transaction reference
        ref_prefix = "CASH" if method == PaymentMethod.CASH else ("UPI" if method == PaymentMethod.UPI else "CARD")
        txn_ref = f"DF-{ref_prefix}-{timezone.now().strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:6].upper()}"

        payment = Payment.objects.create(
            order=order,
            invoice=invoice,
            amount=amount,
            payment_method=method,
            status=PaymentStatus.SUCCESS,
            transaction_reference=txn_ref,
            card_last4=card_last4,
            card_network=card_network,
            upi_vpa=upi_vpa,
            cashier=request.user
        )

        # Mark order and invoice as paid
        order.is_paid = True
        order.status = OrderStatus.COMPLETED
        order.completed_at = timezone.now()
        order.save(update_fields=['is_paid', 'status', 'completed_at'])

        invoice.is_paid = True
        invoice.payment_method = method
        invoice.save(update_fields=['is_paid', 'payment_method'])

        # Free table if occupied
        if order.table:
            order.table.status = TableStatus.CLEANING
            order.table.current_order = None
            order.table.save(update_fields=['status', 'current_order'])

        messages.success(request, f"Payment of ₹{payment.amount} recorded via {payment.get_payment_method_display()} (Ref: {payment.transaction_reference})")
        return redirect('billing:thermal', invoice_id=invoice.id)

    # QR Payload simulation for UPI
    upi_string = f"upi://pay?pa=dineflow.internal@icici&pn={order.branch.name}&am={invoice.grand_total}&cu=INR&tn=Bill-{invoice.invoice_number}"

    return render(request, 'payments/checkout.html', {
        'order': order,
        'invoice': invoice,
        'payment_methods': PaymentMethod.choices,
        'upi_string': upi_string,
    })

@login_required
@module_permission_required('payments')
def payment_list_view(request):
    """Ledger of all collected payments across methods."""
    branch = request.user.branch
    payments = Payment.objects.all().select_related('order', 'invoice', 'cashier')
    
    if branch:
        payments = payments.filter(order__branch=branch)
        
    method_filter = request.GET.get('method')
    date_filter = request.GET.get('date')
    
    if method_filter:
        payments = payments.filter(payment_method=method_filter)
    if date_filter:
        payments = payments.filter(created_at__date=date_filter)

    payments = payments.order_by('-created_at')
    
    total_collected = sum(p.amount for p in payments if p.status == PaymentStatus.SUCCESS)

    return render(request, 'payments/payment_list.html', {
        'payments': payments,
        'total_collected': total_collected,
        'method_filter': method_filter,
        'date_filter': date_filter,
        'payment_methods': PaymentMethod.choices,
    })
