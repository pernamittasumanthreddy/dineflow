from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Restaurant, Branch, User


class Menu(BaseModel):
    MENU_TYPES = [
        ('DINE_IN', 'Dine-in'),
        ('TAKEAWAY', 'Takeaway'),
        ('DELIVERY', 'Delivery'),
        ('BAR', 'Bar'),
        ('ALL', 'All Channels'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='menus')
    name = models.CharField(max_length=100)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES, default='ALL')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_menus'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        branch_str = f" - {self.branch.name}" if self.branch else " (All Branches)"
        return f"{self.name}{branch_str}"


class MenuCategory(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='menu/categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_menu_categories'
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.menu.name} > {self.name}"


class MenuItem(BaseModel):
    DIETARY_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('EGG', 'Contains Egg'),
        ('VEGAN', 'Vegan'),
        ('JAIN', 'Jain Friendly'),
    ]

    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=150, db_index=True)
    short_code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    dietary_type = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='VEG', db_index=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time_minutes = models.PositiveIntegerField(default=15)
    calorie_count = models.PositiveIntegerField(null=True, blank=True)
    hsn_code = models.CharField(max_length=10, default='996331', help_text="GST HSN/SAC Code for Restaurant Service")
    is_available = models.BooleanField(default=True, db_index=True)
    is_recommended = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu/items/', null=True, blank=True)

    class Meta:
        db_table = 'df_menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        constraints = [
            CheckConstraint(condition=Q(base_price__gte=0), name='menu_item_base_price_non_negative')
        ]
        indexes = [
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['dietary_type', 'is_available']),
        ]

    def __str__(self):
        return f"{self.name} (₹{self.base_price})"


class MenuVariant(BaseModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=50)  # e.g., 'Regular', 'Half', 'Full', 'Large'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True)
    is_default = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_menu_variants'
        verbose_name = 'Menu Variant'
        verbose_name_plural = 'Menu Variants'
        constraints = [
            CheckConstraint(condition=Q(price__gte=0), name='menu_variant_price_non_negative'),
            models.UniqueConstraint(fields=['menu_item', 'name'], name='unique_item_variant_name')
        ]

    def __str__(self):
        return f"{self.menu_item.name} - {self.name} (₹{self.price})"


class MenuAddon(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_menu_addons'
        verbose_name = 'Menu Addon'
        verbose_name_plural = 'Menu Addons'
        constraints = [
            CheckConstraint(condition=Q(price__gte=0), name='addon_price_non_negative')
        ]

    def __str__(self):
        return f"{self.name} (+₹{self.price})"


class MenuItemAddon(BaseModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='item_addons')
    addon = models.ForeignKey(MenuAddon, on_delete=models.CASCADE, related_name='menu_items')
    is_free = models.BooleanField(default=False)
    max_quantity = models.PositiveSmallIntegerField(default=5)

    class Meta:
        db_table = 'df_menu_item_addons'
        verbose_name = 'Menu Item Addon'
        verbose_name_plural = 'Menu Item Addons'
        constraints = [
            models.UniqueConstraint(fields=['menu_item', 'addon'], name='unique_menu_item_addon')
        ]

    def __str__(self):
        return f"{self.menu_item.name} -> {self.addon.name}"


class PriceHistory(BaseModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='price_history')
    menu_variant = models.ForeignKey(
        MenuVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='price_history'
    )
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_from = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='price_changes'
    )
    reason = models.TextField(blank=True)

    class Meta:
        db_table = 'df_price_history'
        verbose_name = 'Price History'
        verbose_name_plural = 'Price Histories'
        ordering = ['-effective_from']

    def __str__(self):
        return f"{self.menu_item.name}: ₹{self.old_price} -> ₹{self.new_price}"


class Recipe(BaseModel):
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE, related_name='recipe')
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    prep_time_minutes = models.PositiveIntegerField(default=10)
    cook_time_minutes = models.PositiveIntegerField(default=20)
    yield_servings = models.PositiveIntegerField(default=1)
    target_temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'df_recipes'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"Recipe for {self.menu_item.name}"


class FoodIngredient(BaseModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    inventory_item = models.ForeignKey(
        'inventory.InventoryItem', on_delete=models.PROTECT, related_name='food_recipes'
    )
    quantity_required = models.DecimalField(
        max_digits=10, decimal_places=3, help_text="Quantity in item measurement unit"
    )
    unit_name = models.CharField(max_length=20)
    wastage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_food_ingredients'
        verbose_name = 'Food Ingredient (BOM)'
        verbose_name_plural = 'Food Ingredients (BOM)'
        constraints = [
            CheckConstraint(condition=Q(quantity_required__gt=0), name='ingredient_qty_positive'),
            CheckConstraint(
                condition=Q(wastage_percentage__gte=0) & Q(wastage_percentage__lte=100),
                name='ingredient_wastage_valid'
            )
        ]

    def __str__(self):
        return f"{self.inventory_item.name}: {self.quantity_required} {self.unit_name} for {self.recipe.menu_item.name}"
