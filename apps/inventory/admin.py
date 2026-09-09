from django.contrib import admin
from .models import (
    Unit, InventoryCategory, InventoryItem, Ingredient,
    Stock, StockBatch, StockMovement, StockAdjustment,
    ExpiryRecord, WasteRecord, InventoryAlert
)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'is_base_unit']


@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'restaurant']
    list_filter = ['restaurant']


class IngredientInline(admin.StackedInline):
    model = Ingredient
    can_delete = False


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_code', 'restaurant', 'category', 'primary_unit', 'reorder_level', 'is_active']
    list_filter = ['restaurant', 'category', 'is_active', 'is_perishable']
    search_fields = ['name', 'item_code']
    inlines = [IngredientInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'branch', 'quantity_on_hand', 'available_quantity']
    list_filter = ['branch']
    search_fields = ['inventory_item__name', 'inventory_item__item_code']


@admin.register(StockBatch)
class StockBatchAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'inventory_item', 'branch', 'expiry_date', 'remaining_quantity']
    list_filter = ['branch', 'expiry_date']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'branch', 'movement_type', 'quantity', 'balance_after', 'created_at']
    list_filter = ['branch', 'movement_type', 'created_at']
    search_fields = ['inventory_item__name', 'reference_id']


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'branch', 'adjustment_type', 'quantity', 'reason', 'cost_impact']
    list_filter = ['branch', 'adjustment_type', 'reason']


@admin.register(WasteRecord)
class WasteRecordAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'branch', 'quantity', 'cost_impact', 'created_at']
    list_filter = ['branch', 'created_at']


@admin.register(InventoryAlert)
class InventoryAlertAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'branch', 'alert_type', 'is_resolved', 'created_at']
    list_filter = ['branch', 'alert_type', 'is_resolved']
