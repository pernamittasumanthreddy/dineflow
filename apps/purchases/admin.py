"""Purchases Django Admin."""
from django.contrib import admin
from apps.purchases.models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0
    readonly_fields = ('item_total', 'gst_amount')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'branch', 'status', 'total_amount', 'order_date', 'received_at')
    list_filter = ('branch', 'status', 'order_date')
    search_fields = ('po_number', 'supplier__company_name')
    inlines = [PurchaseOrderItemInline]
