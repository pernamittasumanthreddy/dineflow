"""Offline-First Multi-Method Payment Ledger & Simulation Models."""
import uuid
from decimal import Decimal
from django.db import models
from apps.core.models import TimeStampedModel

class PaymentMethod(models.TextChoices):
    CASH = 'CASH', 'Cash'
    UPI = 'UPI', 'UPI (Google Pay / PhonePe / Paytm)'
    CARD = 'CARD', 'Credit / Debit Card'
    SPLIT = 'SPLIT', 'Split Payment'

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUCCESS = 'SUCCESS', 'Settled / Successful'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'

class Payment(TimeStampedModel):
    """Transaction record for settled dining orders."""
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey('billing.Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField('Amount Paid (₹)', max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.SUCCESS, db_index=True)
    
    # Internal transaction reference (no external API needed)
    transaction_reference = models.CharField('Transaction Ref / UTR', max_length=100, unique=True, db_index=True)
    upi_vpa = models.CharField('Payer UPI VPA', max_length=100, blank=True)
    card_last4 = models.CharField('Card Last 4 Digits', max_length=4, blank=True)
    card_network = models.CharField('Card Network', max_length=30, blank=True, help_text='Visa, Mastercard, RuPay')
    
    cashier = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Payment Record'
        verbose_name_plural = 'Payment Records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_payment_method_display()} - ₹{self.amount} ({self.transaction_reference})"

    def save(self, *args, **kwargs):
        if not self.transaction_reference:
            prefix = "TXN-CASH" if self.payment_method == PaymentMethod.CASH else ("TXN-UPI" if self.payment_method == PaymentMethod.UPI else "TXN-POS")
            self.transaction_reference = f"{prefix}-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
