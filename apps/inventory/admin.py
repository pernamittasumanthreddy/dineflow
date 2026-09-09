"""Inventory Django Admin."""
from django.contrib import admin
from apps.inventory.models import IngredientCategory, Ingredient, StockMovement

@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'category', 'current_stock', 'unit', 'minimum_stock_level', 'unit_cost', 'is_low_stock')
    list_filter = ('branch', 'category', 'unit')
    search_fields = ('name', 'code', 'batch_number')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'movement_type', 'quantity', 'stock_before', 'stock_after', 'reference_id', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('ingredient__name', 'reference_id')
    readonly_fields = ('ingredient', 'movement_type', 'quantity', 'stock_before', 'stock_after', 'reference_id', 'recorded_by', 'created_at')
