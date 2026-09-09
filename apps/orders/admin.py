from django.contrib import admin

from .models import (
    Order,
    OrderDiscount,
    OrderItem,
    OrderStatusHistory,
    OrderTax,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderTaxInline(admin.TabularInline):
    model = OrderTax
    extra = 0


class OrderDiscountInline(admin.TabularInline):
    model = OrderDiscount
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'branch', 'order_type', 'status', 'final_amount', 'placed_at']
    list_filter = ['branch', 'order_type', 'status', 'placed_at']
    search_fields = ['order_number', 'customer__name', 'customer__phone']
    inlines = [OrderItemInline, OrderTaxInline, OrderDiscountInline]


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'old_status', 'new_status', 'changed_by', 'timestamp']
    list_filter = ['new_status', 'timestamp']
