"""Comprehensive Inventory, Raw Materials, and Auditable Stock Movement Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, SoftDeleteModel

class UnitOfMeasure(models.TextChoices):
    KILOGRAM = 'kg', 'Kilogram (kg)'
    GRAM = 'g', 'Gram (g)'
    LITER = 'L', 'Liter (L)'
    MILLILITER = 'ml', 'Milliliter (ml)'
    PIECE = 'pcs', 'Pieces (pcs)'
    PACK = 'pack', 'Pack (pack)'
    DOZEN = 'dz', 'Dozen (dz)'

class IngredientCategory(TimeStampedModel):
    """Classification of raw materials (Vegetables, Poultry, Dairy, Spices, Grains, Oils)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Ingredient Category'
        verbose_name_plural = 'Ingredient Categories'

    def __str__(self):
        return self.name

class IngredientQuerySet(models.QuerySet):
    def with_category(self):
        """Optimizes queries by joining category and branch."""
        return self.select_related('category', 'branch')

    def low_stock(self):
        """Returns ingredients where current stock is at or below minimum reorder level."""
        return self.filter(current_stock__lte=models.F('minimum_stock_level'))

class Ingredient(TimeStampedModel, SoftDeleteModel):
    """Raw ingredient or material stocked at a branch."""
    objects = IngredientQuerySet.as_manager()
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='ingredients',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        IngredientCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredients'
    )
    name = models.CharField('Ingredient Name', max_length=150, db_index=True)
    code = models.CharField('SKU / Code', max_length=50, blank=True)
    unit = models.CharField('Unit', max_length=10, choices=UnitOfMeasure.choices, default=UnitOfMeasure.KILOGRAM)
    
    # Stock levels
    current_stock = models.DecimalField('Current Stock Level', max_digits=12, decimal_places=3, default=Decimal('0.000'))
    minimum_stock_level = models.DecimalField('Reorder / Low Stock Level', max_digits=12, decimal_places=3, default=Decimal('10.000'))
    optimal_stock_level = models.DecimalField('Max / Optimal Stock', max_digits=12, decimal_places=3, default=Decimal('100.000'))
    
    # Costing
    unit_cost = models.DecimalField('Unit Cost (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Batch tracking
    batch_number = models.CharField('Batch #', max_length=50, blank=True)
    expiry_date = models.DateField('Expiry Date', null=True, blank=True)

    class Meta:
        verbose_name = 'Raw Ingredient'
        verbose_name_plural = 'Raw Ingredients'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock_level

    @property
    def stock_value(self):
        return self.current_stock * self.unit_cost

class MovementType(models.TextChoices):
    OPENING_STOCK = 'OPENING_STOCK', 'Opening Stock'
    PURCHASE_RECEIPT = 'PURCHASE_RECEIPT', 'Purchase Inward'
    ORDER_CONSUMPTION = 'ORDER_CONSUMPTION', 'Recipe Consumption'
    WASTE_SPOILAGE = 'WASTE_SPOILAGE', 'Waste / Spoilage'
    AUDIT_ADJUSTMENT = 'AUDIT_ADJUSTMENT', 'Physical Count Adjustment'
    BRANCH_TRANSFER = 'BRANCH_TRANSFER', 'Branch Transfer'

class StockMovement(TimeStampedModel):
    """Immutable audit ledger of all inventory additions and deductions."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=30, choices=MovementType.choices)
    quantity = models.DecimalField(
        'Quantity Delta (+ or -)',
        max_digits=12,
        decimal_places=3,
        help_text='Positive for intake, negative for consumption/waste'
    )
    stock_before = models.DecimalField(max_digits=12, decimal_places=3)
    stock_after = models.DecimalField(max_digits=12, decimal_places=3)
    reference_id = models.CharField('Order # / PO # / Reason', max_length=100, blank=True)
    recorded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements'
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ingredient.name} [{self.get_movement_type_display()}]: {self.quantity} {self.ingredient.unit}"
