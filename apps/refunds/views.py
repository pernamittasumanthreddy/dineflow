"""Refund Management, Dual Approval Workflow, and Disbursal Views."""
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.refunds.models import RefundRequest, RefundStatus
from apps.payments.models import Payment, PaymentStatus
from apps.orders.models import Order
from apps.accounts.decorators import module_permission_required, role_required
from apps.accounts.models import RoleChoices

@login_required
@module_permission_required('refunds')
def refund_request_view(request, payment_id):
    """Cashier submits a refund request requiring manager approval."""
    payment = get_object_or_404(Payment.objects.select_related('order'), id=payment_id)
    
    if request.method == 'POST':
        amount_str = request.POST.get('amount', str(payment.amount))
        amount = Decimal(amount_str)
        reason = request.POST.get('reason', '').strip()
        
        if not reason:
            messages.error(request, "Reason for refund is mandatory for audit compliance.")
            return redirect('refunds:request', payment_id=payment.id)
            
        if amount > payment.amount:
            messages.error(request, "Refund amount cannot exceed original payment amount.")
            return redirect('refunds:request', payment_id=payment.id)

        now = timezone.now()
        ref_count = RefundRequest.objects.count() + 1
        ref_num = f"REF-{now.strftime('%Y%m%d')}-{ref_count:04d}"

        refund = RefundRequest.objects.create(
            refund_number=ref_num,
            order=payment.order,
            payment=payment,
            amount=amount,
            reason=reason,
            status=RefundStatus.PENDING,
            requested_by=request.user
        )

        messages.success(request, f"Refund request #{refund.refund_number} submitted for Manager approval.")
        return redirect('refunds:list')

    return render(request, 'refunds/refund_form.html', {'payment': payment})

@login_required
@role_required(RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER, RoleChoices.SUPER_ADMIN)
def refund_approval_view(request, refund_id):
    """Manager approves or rejects refund."""
    refund = get_object_or_404(RefundRequest.objects.select_related('payment', 'order'), id=refund_id)
    
    if request.method == 'POST':
        decision = request.POST.get('decision')
        notes = request.POST.get('manager_notes', '')
        
        if decision == 'APPROVE':
            refund.status = RefundStatus.APPROVED
            refund.approved_by = request.user
            refund.manager_notes = notes
            refund.processed_at = timezone.now()
            refund.save()

            # Mark payment as refunded
            refund.payment.status = PaymentStatus.REFUNDED
            refund.payment.save(update_fields=['status'])

            messages.success(request, f"Refund #{refund.refund_number} of ₹{refund.amount} approved and recorded.")
        elif decision == 'REJECT':
            refund.status = RefundStatus.REJECTED
            refund.approved_by = request.user
            refund.manager_notes = notes
            refund.save()
            messages.warning(request, f"Refund #{refund.refund_number} was rejected.")

    return redirect('refunds:list')

@login_required
@module_permission_required('refunds')
def refund_list_view(request):
    """List of all refund vouchers and audit statuses."""
    branch = request.user.branch
    refunds = RefundRequest.objects.all().select_related('order', 'payment', 'requested_by', 'approved_by')
    
    if branch:
        refunds = refunds.filter(order__branch=branch)
        
    status_filter = request.GET.get('status')
    if status_filter:
        refunds = refunds.filter(status=status_filter)
        
    refunds = refunds.order_by('-created_at')

    return render(request, 'refunds/refund_list.html', {
        'refunds': refunds,
        'status_filter': status_filter,
        'statuses': RefundStatus.choices,
    })
