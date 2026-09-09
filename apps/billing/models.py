from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Restaurant, Branch, User


class InvoiceNumberSequence(BaseModel):
    """
    Concurrency-safe sequence generator for Indian tax invoices.
    Uses pessimistic row locking in billing service to guarantee no gaps or duplicate numbers.
    """
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='invoice_sequences')
    fiscal_year = models.CharField(max_length=10, help_text="e.g. 2026-27")
    prefix = models.CharField(max_length=10, default='INV')
    last_number = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'df_invoice_sequences'
        verbose_name = 'Invoice Number Sequence'
        verbose_name_plural = 'Invoice Number Sequences'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'fiscal_year', 'prefix'], name='unique_invoice_seq_per_branch_fy')
        ]

    def __str__(self):
        return f"{self.branch.code}/{self.prefix}/{self.fiscal_year}/{self.last_number:05d}"


class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('ISSUED', 'Issued'),
        ('PAID', 'Paid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    order = models.OneToOneField('orders.Order', on_delete=models.PROTECT, related_name='invoice')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='invoices')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='invoices')
    invoice_number = models.CharField(max_length=60, unique=True, db_index=True)
    fiscal_year = models.CharField(max_length=10, db_index=True)
    invoice_date = models.DateTimeField(default=timezone.now, db_index=True)

    # Customer info at invoice time
    customer_name = models.CharField(max_length=150, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_gstin = models.CharField(max_length=15, blank=True)

    # Financial breakdown
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # GST Components (Indian Standard)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    service_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    round_off = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ISSUED', db_index=True)
    qr_code_data = models.TextField(blank=True, help_text="B2C UPI / GST e-Invoice payload")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        constraints = [
            CheckConstraint(condition=Q(subtotal__gte=0), name='invoice_subtotal_non_negative'),
            CheckConstraint(condition=Q(taxable_amount__gte=0), name='invoice_taxable_non_negative'),
            CheckConstraint(condition=Q(grand_total__gte=0), name='invoice_grand_total_non_negative'),
            CheckConstraint(condition=Q(cgst_amount__gte=0), name='invoice_cgst_non_negative'),
            CheckConstraint(condition=Q(sgst_amount__gte=0), name='invoice_sgst_non_negative'),
            CheckConstraint(condition=Q(igst_amount__gte=0), name='invoice_igst_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'invoice_date']),
            models.Index(fields=['branch', 'status', 'invoice_date']),
        ]

    def __str__(self):
        return f"Invoice {self.invoice_number} - ₹{self.grand_total} [{self.status}]"


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=150)
    hsn_sac_code = models.CharField(max_length=10, default='996331')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)

    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'df_invoice_items'
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='inv_item_qty_positive'),
            CheckConstraint(condition=Q(unit_price__gte=0), name='inv_item_unit_price_non_negative'),
            CheckConstraint(condition=Q(total_amount__gte=0), name='inv_item_total_non_negative'),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.item_name} (₹{self.total_amount})"


class InvoiceTax(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='tax_breakdowns')
    tax_category_name = models.CharField(max_length=100)
    component_name = models.CharField(max_length=20)  # CGST, SGST, IGST
    rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'df_invoice_taxes'
        verbose_name = 'Invoice Tax Breakdown'
        verbose_name_plural = 'Invoice Tax Breakdowns'

    def __str__(self):
        return f"{self.component_name} @ {self.rate_percent}% on ₹{self.taxable_amount}: ₹{self.tax_amount}"


class InvoiceDiscount(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='discounts')
    description = models.CharField(max_length=150)
    rate_or_flat = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'df_invoice_discounts'
        verbose_name = 'Invoice Discount'
        verbose_name_plural = 'Invoice Discounts'

    def __str__(self):
        return f"{self.description}: ₹{self.discount_amount}"
