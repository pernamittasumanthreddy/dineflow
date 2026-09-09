from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Restaurant, Branch, User


class Unit(BaseModel):
    name = models.CharField(max_length=50)  # e.g., Kilogram, Gram, Litre, Millilitre, Piece
    symbol = models.CharField(max_length=10, unique=True)  # e.g., kg, g, l, ml, pcs
    is_base_unit = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_units'
        verbose_name = 'Unit of Measurement'
        verbose_name_plural = 'Units of Measurement'

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class InventoryCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='inventory_categories')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'df_inventory_categories'
        verbose_name = 'Inventory Category'
        verbose_name_plural = 'Inventory Categories'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'code'], name='unique_inv_category_per_restaurant')
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class InventoryItem(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='inventory_items')
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150, db_index=True)
    item_code = models.CharField(max_length=50, db_index=True)
    primary_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='inventory_items')
    reorder_level = models.DecimalField(max_digits=12, decimal_places=3, default=10.000)
    safety_stock = models.DecimalField(max_digits=12, decimal_places=3, default=5.000)
    current_cost_per_unit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_perishable = models.BooleanField(default=False)
    shelf_life_days = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_inventory_items'
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'item_code'], name='unique_item_code_per_restaurant'),
            CheckConstraint(condition=Q(reorder_level__gte=0), name='inv_reorder_level_non_negative'),
            CheckConstraint(condition=Q(current_cost_per_unit__gte=0), name='inv_cost_non_negative'),
        ]
        indexes = [
            models.Index(fields=['restaurant', 'category', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.item_code}) - {self.primary_unit.symbol}"


class Ingredient(BaseModel):
    inventory_item = models.OneToOneField(InventoryItem, on_delete=models.CASCADE, related_name='ingredient_details')
    culinary_name = models.CharField(max_length=150)
    storage_temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    yield_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    allergens = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'df_ingredients'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            CheckConstraint(
                condition=Q(yield_percentage__gt=0) & Q(yield_percentage__lte=100),
                name='ingredient_yield_valid_percent'
            )
        ]

    def __str__(self):
        return f"{self.culinary_name} (Yield: {self.yield_percentage}%)"


class Stock(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stock_levels')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='branch_stocks')
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    reserved_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    available_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    last_stock_take_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'df_stocks'
        verbose_name = 'Stock Level'
        verbose_name_plural = 'Stock Levels'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'inventory_item'], name='unique_stock_per_branch_item'),
            CheckConstraint(condition=Q(quantity_on_hand__gte=0), name='stock_on_hand_non_negative'),
            CheckConstraint(condition=Q(available_quantity__gte=0), name='stock_available_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'inventory_item']),
        ]

    def __str__(self):
        return f"{self.inventory_item.name} at {self.branch.name}: {self.quantity_on_hand} {self.inventory_item.primary_unit.symbol}"


class StockBatch(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stock_batches')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    received_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True, db_index=True)
    purchase_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    remaining_quantity = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        db_table = 'df_stock_batches'
        verbose_name = 'Stock Batch'
        verbose_name_plural = 'Stock Batches'
        constraints = [
            CheckConstraint(condition=Q(remaining_quantity__gte=0), name='batch_remaining_qty_non_negative'),
            CheckConstraint(condition=Q(purchase_unit_price__gte=0), name='batch_unit_price_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'expiry_date']),
        ]

    def __str__(self):
        return f"Batch {self.batch_number} - {self.inventory_item.name} ({self.remaining_quantity}/{self.initial_quantity})"


class StockMovement(BaseModel):
    MOVEMENT_TYPES = [
        ('PURCHASE_RECEIPT', 'Purchase Receipt'),
        ('RECIPE_CONSUMPTION', 'Recipe Consumption'),
        ('WASTAGE', 'Wastage / Spoilage'),
        ('ADJUSTMENT_ADD', 'Adjustment (Addition)'),
        ('ADJUSTMENT_SUB', 'Adjustment (Deduction)'),
        ('RETURN_TO_SUPPLIER', 'Return to Supplier'),
        ('BRANCH_TRANSFER_IN', 'Branch Transfer In'),
        ('BRANCH_TRANSFER_OUT', 'Branch Transfer Out'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stock_movements')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='movements')
    batch = models.ForeignKey(
        StockBatch, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements'
    )
    movement_type = models.CharField(max_length=30, choices=MOVEMENT_TYPES, db_index=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, help_text="+ for addition, - for reduction")
    balance_before = models.DecimalField(max_digits=12, decimal_places=3)
    balance_after = models.DecimalField(max_digits=12, decimal_places=3)
    reference_id = models.CharField(max_length=100, blank=True, help_text="e.g. Order #, PO #, GRN #")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        indexes = [
            models.Index(fields=['branch', 'inventory_item', 'created_at']),
            models.Index(fields=['movement_type', 'created_at']),
        ]

    def __str__(self):
        sign = "+" if self.quantity > 0 else ""
        return f"{self.branch.name} | {self.inventory_item.name} {sign}{self.quantity} [{self.movement_type}]"


class StockAdjustment(BaseModel):
    ADJUSTMENT_REASONS = [
        ('DAMAGE', 'Damaged Stock'),
        ('EXPIRED', 'Expired Stock'),
        ('AUDIT_VARIANCE', 'Audit / Physical Count Variance'),
        ('THEFT', 'Theft / Pilferage'),
        ('OTHER', 'Other Reason'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stock_adjustments')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='adjustments')
    adjustment_type = models.CharField(max_length=10, choices=[('INCREASE', 'Increase'), ('DECREASE', 'Decrease')])
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    reason = models.CharField(max_length=30, choices=ADJUSTMENT_REASONS)
    cost_impact = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_stock_adjustments'
        verbose_name = 'Stock Adjustment'
        verbose_name_plural = 'Stock Adjustments'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='adjustment_qty_positive'),
        ]

    def __str__(self):
        return f"Adj {self.adjustment_type} {self.quantity} for {self.inventory_item.name} ({self.reason})"


class ExpiryRecord(BaseModel):
    batch = models.ForeignKey(StockBatch, on_delete=models.CASCADE, related_name='expiry_records')
    expired_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    recorded_date = models.DateField(default=timezone.now)
    action_taken = models.CharField(
        max_length=30,
        choices=[('DISCARDED', 'Discarded'), ('DONATED', 'Donated'), ('RETURNED', 'Returned to Vendor')]
    )
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_expiry_records'
        verbose_name = 'Expiry Record'
        verbose_name_plural = 'Expiry Records'

    def __str__(self):
        return f"Expired {self.expired_quantity} from Batch {self.batch.batch_number} [{self.action_taken}]"


class WasteRecord(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='waste_records')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='waste_records')
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    reason = models.TextField()
    cost_impact = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_waste_records'
        verbose_name = 'Waste Record'
        verbose_name_plural = 'Waste Records'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='waste_qty_positive'),
            CheckConstraint(condition=Q(cost_impact__gte=0), name='waste_cost_non_negative'),
        ]

    def __str__(self):
        return f"Waste {self.quantity} {self.inventory_item.name} (₹{self.cost_impact})"


class InventoryAlert(BaseModel):
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock Threshold'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('NEAR_EXPIRY', 'Near Expiry Date'),
        ('EXPIRED', 'Expired Stock'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory_alerts')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES, db_index=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'df_inventory_alerts'
        verbose_name = 'Inventory Alert'
        verbose_name_plural = 'Inventory Alerts'
        indexes = [
            models.Index(fields=['branch', 'is_resolved']),
        ]

    def __str__(self):
        return f"[{self.alert_type}] {self.inventory_item.name} - {self.branch.name}"
