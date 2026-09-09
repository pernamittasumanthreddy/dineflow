"""Orders Django Admin Registration."""
from django.contrib import admin
from apps.orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_total',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'branch', 'order_type', 'table', 'status', 'grand_total', 'is_paid', 'created_at')
    list_filter = ('branch', 'order_type', 'status', 'is_paid', 'created_at')
    search_fields = ('order_number', 'customer__name', 'customer__phone')
    inlines = [OrderItemInline]
