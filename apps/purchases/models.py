from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent to Supplier'),
        ('PARTIALLY_RECEIVED', 'Partially Received'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='purchase_orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchase_orders')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, related_name='purchase_orders')
    po_number = models.CharField(max_length=50, unique=True, db_index=True)
    order_date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT', db_index=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    terms_and_conditions = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_purchase_orders'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        constraints = [
            CheckConstraint(condition=Q(subtotal__gte=0), name='po_subtotal_non_negative'),
            CheckConstraint(condition=Q(tax_amount__gte=0), name='po_tax_non_negative'),
            CheckConstraint(condition=Q(total_amount__gte=0), name='po_total_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'status', 'order_date']),
        ]

    def __str__(self):
        return f"PO #{self.po_number} - {self.supplier.name} (₹{self.total_amount}) [{self.status}]"


class PurchaseOrderItem(BaseModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem', on_delete=models.PROTECT, related_name='po_items'
    )
    quantity_ordered = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_received = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'df_purchase_order_items'
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'
        constraints = [
            CheckConstraint(condition=Q(quantity_ordered__gt=0), name='po_item_qty_ordered_positive'),
            CheckConstraint(condition=Q(unit_price__gte=0), name='po_item_unit_price_non_negative'),
            CheckConstraint(condition=Q(total_amount__gte=0), name='po_item_total_non_negative'),
        ]

    def __str__(self):
        return f"{self.quantity_ordered} {self.inventory_item.primary_unit.symbol} of {self.inventory_item.name}"


class GoodsReceipt(BaseModel):
    STATUS_CHOICES = [
        ('PENDING_INSPECTION', 'Pending Inspection'),
        ('VERIFIED', 'Verified & Inwarded'),
        ('REJECTED', 'Rejected'),
    ]

    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods_receipts'
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='goods_receipts')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='goods_receipts')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, related_name='goods_receipts')
    grn_number = models.CharField(max_length=50, unique=True, db_index=True)
    received_date = models.DateField(default=timezone.now)
    delivery_challan_number = models.CharField(max_length=100, blank=True)
    supplier_invoice_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_INSPECTION', db_index=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_goods_receipts'
        verbose_name = 'Goods Receipt (GRN)'
        verbose_name_plural = 'Goods Receipts (GRN)'
        indexes = [
            models.Index(fields=['branch', 'status', 'received_date']),
        ]

    def __str__(self):
        return f"GRN #{self.grn_number} from {self.supplier.name} [{self.status}]"


class GoodsReceiptItem(BaseModel):
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='items')
    po_item = models.ForeignKey(
        PurchaseOrderItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='grn_items'
    )
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem', on_delete=models.PROTECT, related_name='grn_items'
    )
    quantity_received = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_accepted = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_rejected = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'df_goods_receipt_items'
        verbose_name = 'Goods Receipt Item'
        verbose_name_plural = 'Goods Receipt Items'
        constraints = [
            CheckConstraint(condition=Q(quantity_received__gte=0), name='grn_item_received_non_negative'),
            CheckConstraint(condition=Q(quantity_accepted__gte=0), name='grn_item_accepted_non_negative'),
            CheckConstraint(condition=Q(quantity_rejected__gte=0), name='grn_item_rejected_non_negative'),
        ]

    def __str__(self):
        return f"GRN Item: {self.inventory_item.name} - Accepted {self.quantity_accepted}"


class PurchasePayment(BaseModel):
    PAYMENT_METHODS = [
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
        ('UPI', 'UPI'),
        ('CASH', 'Cash'),
    ]

    goods_receipt = models.ForeignKey(
        GoodsReceipt, on_delete=models.CASCADE, null=True, blank=True, related_name='payments'
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='payments'
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='BANK_TRANSFER')
    transaction_reference = models.CharField(max_length=100)
    payment_date = models.DateField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_purchase_payments'
        verbose_name = 'Purchase Payment'
        verbose_name_plural = 'Purchase Payments'
        constraints = [
            CheckConstraint(condition=Q(amount_paid__gt=0), name='purchase_payment_amt_positive')
        ]

    def __str__(self):
        return f"Paid ₹{self.amount_paid} ref: {self.transaction_reference} on {self.payment_date}"
