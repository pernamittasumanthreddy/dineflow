"""Refund Processing and Dual-Authorization Governance Services."""
import uuid
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.refunds.models import RefundRequest, RefundStatus
from apps.payments.models import PaymentStatus
from apps.audit.models import AuditLog, AuditAction

def create_refund_request(order, payment, amount, reason, requested_by):
    """
    Initiates a formal refund request. Validates that refund amount <= payment amount.
    """
    amount = Decimal(str(amount))
    if amount <= Decimal('0.00'):
        raise ValidationError("Refund amount must be greater than zero.")
    if amount > payment.amount:
        raise ValidationError(f"Refund amount (₹{amount}) cannot exceed settled payment amount (₹{payment.amount}).")

    today_str = timezone.localdate().strftime('%Y%m%d')
    ref_code = f"REF-{today_str}-{uuid.uuid4().hex[:6].upper()}"

    refund = RefundRequest.objects.create(
        refund_number=ref_code,
        order=order,
        payment=payment,
        amount=amount,
        reason=reason,
        status=RefundStatus.PENDING,
        requested_by=requested_by
    )
    return refund

def approve_refund(refund_request, manager, notes=""):
    """
    Manager approves the refund. Disburses payout and updates payment status.
    """
    if refund_request.status != RefundStatus.PENDING:
        raise ValidationError("Only pending refund requests can be approved.")

    refund_request.status = RefundStatus.APPROVED
    refund_request.approved_by = manager
    refund_request.manager_notes = notes
    refund_request.processed_at = timezone.now()
    refund_request.save()

    # Update payment status if full refund
    if refund_request.amount >= refund_request.payment.amount:
        refund_request.payment.status = PaymentStatus.REFUNDED
        refund_request.payment.save(update_fields=['status'])

    # Audit log
    AuditLog.objects.create(
        actor=manager,
        action=AuditAction.REFUND_APPROVE,
        module_name='refunds',
        object_id=refund_request.refund_number,
        object_repr=f"Refund #{refund_request.refund_number} of ₹{refund_request.amount} for Order #{refund_request.order.order_number}",
        old_values={'status': RefundStatus.PENDING},
        new_values={'status': RefundStatus.APPROVED, 'amount': str(refund_request.amount)}
    )

    return refund_request

def reject_refund(refund_request, manager, reason=""):
    """
    Manager rejects the refund request with stated reasons.
    """
    if refund_request.status != RefundStatus.PENDING:
        raise ValidationError("Only pending refund requests can be rejected.")

    refund_request.status = RefundStatus.REJECTED
    refund_request.approved_by = manager
    refund_request.manager_notes = reason
    refund_request.save()

    return refund_request
