"""Comprehensive Culinary Menu Management Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, SoftDeleteModel

class FoodType(models.TextChoices):
    VEG = 'VEG', 'Vegetarian'
    NON_VEG = 'NON_VEG', 'Non-Vegetarian'
    EGG = 'EGG', 'Contains Egg'
    VEGAN = 'VEGAN', 'Vegan'

class SpiceLevel(models.TextChoices):
    MILD = 'MILD', 'Mild'
    MEDIUM = 'MEDIUM', 'Medium'
    SPICY = 'SPICY', 'Spicy'
    EXTRA_SPICY = 'EXTRA_SPICY', 'Extra Spicy'

class Category(TimeStampedModel, SoftDeleteModel):
    """Culinary categories (Biryani, Dosa, Curries, Starters, etc.)."""
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='menu_categories',
        null=True,
        blank=True
    )
    name = models.CharField('Category Name', max_length=100)
    slug = models.SlugField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

class MenuItem(TimeStampedModel, SoftDeleteModel):
    """Specific food dish or beverage item."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField('Item Name', max_length=150, db_index=True)
    code = models.CharField('Short Code / SKU', max_length=30, blank=True)
    description = models.TextField(blank=True)
    food_type = models.CharField(max_length=20, choices=FoodType.choices, default=FoodType.VEG)
    spice_level = models.CharField(max_length=20, choices=SpiceLevel.choices, default=SpiceLevel.MEDIUM)
    
    # Financials
    base_price = models.DecimalField('Base Price (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cost_price = models.DecimalField('Est. Cost Price (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_rate_percent = models.DecimalField('GST Rate %', max_digits=5, decimal_places=2, default=Decimal('5.00'))
    
    # Kitchen & Operations
    preparation_time_minutes = models.PositiveIntegerField('Prep Time (Mins)', default=15)
    is_available = models.BooleanField('Available for Ordering', default=True, db_index=True)
    is_featured = models.BooleanField('Chef Recommendation / Featured', default=False)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - ₹{self.base_price}"

class MenuItemVariant(TimeStampedModel):
    """Portion sizes and variants (Single, Full, Half, Jumbo, 1KG)."""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField('Variant Name', max_length=80)  # e.g., 'Half', 'Full', 'Family Pack'
    price = models.DecimalField('Variant Price (₹)', max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Menu Item Variant'
        verbose_name_plural = 'Menu Item Variants'

    def __str__(self):
        return f"{self.menu_item.name} ({self.name}) - ₹{self.price}"

class MenuItemAddon(TimeStampedModel):
    """Add-ons, sides, and customizations (Extra Cheese, Mirchi Ka Salan, Raita)."""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField('Addon Name', max_length=100)
    price = models.DecimalField('Addon Price (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Menu Item Add-on'
        verbose_name_plural = 'Menu Item Add-ons'

    def __str__(self):
        return f"{self.name} (+₹{self.price})"

class RecipeItem(TimeStampedModel):
    """Bill of Materials (BOM) linking a menu item to raw inventory ingredients."""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        'inventory.Ingredient',
        on_delete=models.CASCADE,
        related_name='recipe_usages',
        null=True,
        blank=True
    )
    ingredient_name = models.CharField('Raw Ingredient Name', max_length=120)
    quantity_required = models.DecimalField(
        'Quantity Required per Serving',
        max_digits=10,
        decimal_places=3,
        help_text='e.g., 0.250 for 250 grams or 0.100 for 100ml'
    )
    unit = models.CharField('Unit of Measure', max_length=20, default='kg')

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'

    def __str__(self):
        return f"{self.quantity_required} {self.unit} of {self.ingredient_name} for {self.menu_item.name}"
