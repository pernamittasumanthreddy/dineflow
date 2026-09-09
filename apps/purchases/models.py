"""Purchase Orders, Inward Goods Verification, and Auto-Stock Intake Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class POStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted for Approval'
    APPROVED = 'APPROVED', 'Approved by Manager'
    RECEIVED = 'RECEIVED', 'Goods Inwarded & Stock Updated'
    CANCELLED = 'CANCELLED', 'Cancelled'

class PurchaseOrder(TimeStampedModel):
    """Procurement Order raised with an approved supplier."""
    po_number = models.CharField('PO #', max_length=50, unique=True, db_index=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='purchase_orders')
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='purchase_orders')
    status = models.CharField(max_length=25, choices=POStatus.choices, default=POStatus.DRAFT, db_index=True)
    
    order_date = models.DateField('Order Date')
    expected_delivery_date = models.DateField('Expected Delivery Date', null=True, blank=True)
    
    # Financials
    subtotal = models.DecimalField('Subtotal (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    gst_amount = models.DecimalField('GST Tax (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField('Total PO Amount (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Signatures
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_pos')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_pos')
    received_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='received_pos')
    received_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"PO #{self.po_number} ({self.supplier.company_name}) - ₹{self.total_amount} [{self.status}]"

    def recalculate_totals(self):
        """Recompute PO subtotal, GST, and grand total."""
        sub = sum(it.item_total for it in self.items.all())
        tax = sum(it.gst_amount for it in self.items.all())
        self.subtotal = sub
        self.gst_amount = tax
        self.total_amount = sub + tax
        self.save(update_fields=['subtotal', 'gst_amount', 'total_amount'])

class PurchaseOrderItem(TimeStampedModel):
    """Line item within a purchase order."""
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    ingredient = models.ForeignKey('inventory.Ingredient', on_delete=models.CASCADE, related_name='po_items')
    ordered_quantity = models.DecimalField('Ordered Qty', max_digits=12, decimal_places=3)
    received_quantity = models.DecimalField('Received Qty', max_digits=12, decimal_places=3, default=Decimal('0.000'))
    unit_cost = models.DecimalField('Unit Cost (₹)', max_digits=10, decimal_places=2)
    gst_rate_percent = models.DecimalField('GST %', max_digits=5, decimal_places=2, default=Decimal('5.00'))
    item_total = models.DecimalField('Item Subtotal (₹)', max_digits=12, decimal_places=2)
    gst_amount = models.DecimalField('Item GST (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'

    def save(self, *args, **kwargs):
        self.item_total = (Decimal(str(self.ordered_quantity)) * Decimal(str(self.unit_cost))).quantize(Decimal('0.01'))
        tax_rate = (self.gst_rate_percent or Decimal('5.00')) / Decimal('100.00')
        self.gst_amount = (self.item_total * tax_rate).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
