"""Dual-Approval Refund Voucher and Audit Trail Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class RefundStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Manager Approval'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    PROCESSED = 'PROCESSED', 'Refund Disbursed'

class RefundRequest(TimeStampedModel):
    """Refund workflow with mandatory dual cashier-manager authorization."""
    refund_number = models.CharField('Refund #', max_length=50, unique=True, db_index=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='refund_requests')
    payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE, related_name='refund_requests')
    amount = models.DecimalField('Refund Amount (₹)', max_digits=12, decimal_places=2)
    reason = models.TextField('Reason for Refund', help_text='Mandatory audit reason for refund request')
    status = models.CharField(max_length=20, choices=RefundStatus.choices, default=RefundStatus.PENDING, db_index=True)
    
    # Audit signatures
    requested_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='requested_refunds')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_refunds')
    manager_notes = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Refund Voucher'
        verbose_name_plural = 'Refund Vouchers'
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund {self.refund_number}: ₹{self.amount} for Order #{self.order.order_number} [{self.status}]"
