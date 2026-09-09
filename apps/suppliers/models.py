from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class Supplier(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=150, db_index=True)
    supplier_code = models.CharField(max_length=50)
    gstin = models.CharField(max_length=15, blank=True, help_text="Supplier GSTIN")
    pan_number = models.CharField(max_length=10, blank=True)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    payment_terms_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_suppliers'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'supplier_code'], name='unique_supplier_code_per_restaurant')
        ]

    def __str__(self):
        return f"{self.name} ({self.supplier_code})"


class SupplierContact(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_supplier_contacts'
        verbose_name = 'Supplier Contact'
        verbose_name_plural = 'Supplier Contacts'

    def __str__(self):
        return f"{self.name} ({self.supplier.name})"


class SupplierProduct(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem', on_delete=models.CASCADE, related_name='supplier_products'
    )
    supplier_sku = models.CharField(max_length=50, blank=True)
    contracted_unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    lead_time_days = models.PositiveIntegerField(default=2)
    minimum_order_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=1.000)

    class Meta:
        db_table = 'df_supplier_products'
        verbose_name = 'Supplier Product'
        verbose_name_plural = 'Supplier Products'
        constraints = [
            models.UniqueConstraint(fields=['supplier', 'inventory_item'], name='unique_supplier_inventory_item'),
            CheckConstraint(condition=Q(contracted_unit_price__gte=0), name='contract_price_non_negative'),
            CheckConstraint(condition=Q(minimum_order_quantity__gt=0), name='min_order_qty_positive'),
        ]

    def __str__(self):
        return f"{self.inventory_item.name} from {self.supplier.name} @ ₹{self.contracted_unit_price}"


class SupplierPayment(BaseModel):
    PAYMENT_METHODS = [
        ('BANK_TRANSFER', 'Bank Transfer (NEFT/RTGS)'),
        ('CHEQUE', 'Cheque'),
        ('UPI', 'UPI'),
        ('CASH', 'Cash'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='disbursements')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='supplier_payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='BANK_TRANSFER')
    reference_number = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_supplier_payments'
        verbose_name = 'Supplier Payment'
        verbose_name_plural = 'Supplier Payments'
        constraints = [
            CheckConstraint(condition=Q(amount__gt=0), name='supplier_payment_amt_positive')
        ]

    def __str__(self):
        return f"Payment ₹{self.amount} to {self.supplier.name} on {self.payment_date}"


class SupplierRating(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='ratings')
    quality_rating = models.PositiveSmallIntegerField(help_text="1 to 5")
    delivery_punctuality_rating = models.PositiveSmallIntegerField(help_text="1 to 5")
    pricing_rating = models.PositiveSmallIntegerField(help_text="1 to 5")
    review_comments = models.TextField(blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'df_supplier_ratings'
        verbose_name = 'Supplier Rating'
        verbose_name_plural = 'Supplier Ratings'
        constraints = [
            CheckConstraint(condition=Q(quality_rating__gte=1) & Q(quality_rating__lte=5), name='supplier_quality_range'),
            CheckConstraint(condition=Q(delivery_punctuality_rating__gte=1) & Q(delivery_punctuality_rating__lte=5), name='supplier_punctuality_range'),
            CheckConstraint(condition=Q(pricing_rating__gte=1) & Q(pricing_rating__lte=5), name='supplier_pricing_range'),
        ]

    def __str__(self):
        return f"Rating for {self.supplier.name} on {self.rating_date}"
