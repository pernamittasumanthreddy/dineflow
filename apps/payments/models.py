from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Branch, User


class PaymentMethod(BaseModel):
    code = models.CharField(max_length=30, unique=True)  # CASH, UPI, CARD, NET_BANKING, LOYALTY_POINTS
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_payment_methods'
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return self.name


class Payment(BaseModel):
    STATUS_CHOICES = [
        ('INITIATED', 'Initiated'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
        ('PARTIALLY_REFUNDED', 'Partially Refunded'),
    ]

    invoice = models.ForeignKey('billing.Invoice', on_delete=models.PROTECT, related_name='payments')
    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='payments')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    transaction_reference = models.CharField(
        max_length=100, blank=True,
        help_text="UPI UTR number, Card auth code/last-4, Cash receipt identifier"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS', db_index=True)
    paid_at = models.DateTimeField(default=timezone.now, db_index=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        constraints = [
            CheckConstraint(condition=Q(amount__gt=0), name='payment_amount_positive'),
        ]
        indexes = [
            models.Index(fields=['branch', 'paid_at', 'status']),
        ]

    def __str__(self):
        return f"₹{self.amount} via {self.payment_method.name} ({self.transaction_reference or 'Cash'}) [{self.status}]"


class PaymentTransaction(BaseModel):
    TRANSACTION_TYPES = [
        ('PAYMENT', 'Payment Captured'),
        ('REFUND', 'Refund Issued'),
        ('VOID', 'Transaction Voided'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='PAYMENT')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='SUCCESS')
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_payment_transactions'
        verbose_name = 'Payment Transaction Ledger'
        verbose_name_plural = 'Payment Transaction Ledgers'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.transaction_type} of ₹{self.amount} for Payment #{self.payment.id}"


class RefundReason(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_refund_reasons'
        verbose_name = 'Refund Reason'
        verbose_name_plural = 'Refund Reasons'

    def __str__(self):
        return self.title


class Refund(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='refunds')
    invoice = models.ForeignKey('billing.Invoice', on_delete=models.PROTECT, related_name='refunds')
    refund_number = models.CharField(max_length=50, unique=True, db_index=True)
    reason = models.ForeignKey(RefundReason, on_delete=models.PROTECT, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    refund_mode = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='refunds')
    transaction_reference = models.CharField(max_length=100, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approved_refunds')
    refunded_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_refunds'
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        constraints = [
            CheckConstraint(condition=Q(amount__gt=0), name='refund_amount_positive'),
        ]

    def __str__(self):
        return f"Refund #{self.refund_number}: ₹{self.amount} ({self.reason.title})"
