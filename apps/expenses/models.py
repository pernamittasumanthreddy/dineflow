from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class ExpenseCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_expense_categories'
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'code'], name='unique_expense_cat_per_restaurant')
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Expense(BaseModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING_APPROVAL', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PAID', 'Paid'),
    ]

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('CARD', 'Corporate Card'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='expenses')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='expenses')
    expense_number = models.CharField(max_length=50, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField(default=timezone.now, db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='BANK_TRANSFER')
    vendor_name = models.CharField(max_length=150, blank=True)
    invoice_or_bill_ref = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_APPROVAL', db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        constraints = [
            CheckConstraint(condition=Q(amount__gt=0), name='expense_amount_positive'),
            CheckConstraint(condition=Q(total_amount__gte=models.F('amount')), name='expense_total_gte_amount'),
        ]
        indexes = [
            models.Index(fields=['branch', 'expense_date', 'status']),
        ]

    def __str__(self):
        return f"Expense #{self.expense_number}: {self.title} (₹{self.total_amount}) [{self.status}]"


class ExpenseApproval(BaseModel):
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, related_name='approval')
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approved_expenses')
    status = models.CharField(max_length=20, choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected')])
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_expense_approvals'
        verbose_name = 'Expense Approval'
        verbose_name_plural = 'Expense Approvals'

    def __str__(self):
        return f"Approval for {self.expense.expense_number}: {self.status} by {self.approver.email}"


class ExpenseAttachment(BaseModel):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='expenses/receipts/')
    file_name = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_expense_attachments'
        verbose_name = 'Expense Attachment'
        verbose_name_plural = 'Expense Attachments'

    def __str__(self):
        return f"Attachment: {self.file_name} for {self.expense.expense_number}"
