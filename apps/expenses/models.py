"""Operational Expense Tracking, Petty Cash, and Voucher Approval Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class ExpenseCategory(TimeStampedModel):
    """Operational cost category (LPG Cylinders, Electricity, Petty Cash, Packaging, Maintenance)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Expense(TimeStampedModel):
    """Voucher record for restaurant branch operational outlays."""
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField('Expense Description / Title', max_length=150)
    amount = models.DecimalField('Amount (₹)', max_digits=12, decimal_places=2)
    expense_date = models.DateField('Expense Date')
    payment_mode = models.CharField(
        max_length=20,
        choices=[('CASH', 'Cash'), ('UPI', 'UPI'), ('BANK_TRANSFER', 'Bank Transfer'), ('CARD', 'Corporate Card')],
        default='CASH'
    )
    receipt_image = models.ImageField(upload_to='expense_receipts/', blank=True, null=True)
    
    # Dual-approval governance
    requested_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='requested_expenses')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    is_approved = models.BooleanField(default=False, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Operating Expense'
        verbose_name_plural = 'Operating Expenses'
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.category.name}) on {self.expense_date}"
