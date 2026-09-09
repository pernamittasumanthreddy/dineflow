from django.contrib import admin

from .models import (
    KitchenOrder,
    KitchenOrderItem,
    KitchenStation,
    PreparationTimer,
)


@admin.register(KitchenStation)
class KitchenStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'code', 'printer_ip', 'is_active']
    list_filter = ['branch', 'is_active']


class KitchenOrderItemInline(admin.TabularInline):
    model = KitchenOrderItem
    extra = 0


@admin.register(KitchenOrder)
class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ['kot_number', 'order', 'branch', 'station', 'priority', 'status', 'created_at']
    list_filter = ['branch', 'status', 'priority', 'created_at']
    search_fields = ['kot_number', 'order__order_number']
    inlines = [KitchenOrderItemInline]


@admin.register(PreparationTimer)
class PreparationTimerAdmin(admin.ModelAdmin):
    list_display = ['kitchen_order', 'estimated_duration_minutes', 'start_time', 'actual_ready_time']
