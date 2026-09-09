"""Indian GST Compliant Tax Invoice & Bill Generation Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel
from apps.core.utils import round_inr

class Invoice(TimeStampedModel):
    """Statutory Indian GST Tax Invoice entity."""
    invoice_number = models.CharField('Invoice #', max_length=50, unique=True, db_index=True)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='invoice')
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    # Statutory details frozen at generation time
    restaurant_name = models.CharField(max_length=200)
    restaurant_gstin = models.CharField('GSTIN', max_length=15)
    fssai_number = models.CharField('FSSAI Lic #', max_length=20)
    branch_address = models.TextField()
    
    # Financial breakdowns
    taxable_subtotal = models.DecimalField('Taxable Value (₹)', max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField('Discount (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cgst_amount = models.DecimalField('CGST (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField('SGST (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    igst_amount = models.DecimalField('IGST (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_tax_amount = models.DecimalField('Total GST (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField('Invoice Grand Total (₹)', max_digits=12, decimal_places=2)
    
    # Settlement
    is_paid = models.BooleanField(default=False, db_index=True)
    payment_method = models.CharField('Payment Method', max_length=50, default='PENDING')
    cashier = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_invoices')
    invoice_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tax Invoice'
        verbose_name_plural = 'Tax Invoices'
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} - ₹{self.grand_total} ({'PAID' if self.is_paid else 'UNPAID'})"

class InvoiceItem(TimeStampedModel):
    """Itemized billing line entry on a GST invoice."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=150)
    sac_code = models.CharField('SAC Code', max_length=20, default='996331')
    quantity = models.PositiveIntegerField(default=1)
    unit_rate = models.DecimalField('Rate (₹)', max_digits=10, decimal_places=2)
    item_total = models.DecimalField('Total (₹)', max_digits=12, decimal_places=2)
    tax_rate_percent = models.DecimalField('GST %', max_digits=5, decimal_places=2, default=Decimal('5.00'))
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'

    def __str__(self):
        return f"{self.quantity}x {self.item_name} @ ₹{self.unit_rate}"
