from django.contrib import admin

from .models import (
    GoodsReceipt,
    GoodsReceiptItem,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchasePayment,
)


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'branch', 'supplier', 'order_date', 'total_amount', 'status']
    list_filter = ['branch', 'status', 'order_date']
    search_fields = ['po_number', 'supplier__name']
    inlines = [PurchaseOrderItemInline]


class GoodsReceiptItemInline(admin.TabularInline):
    model = GoodsReceiptItem
    extra = 0


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = ['grn_number', 'purchase_order', 'branch', 'supplier', 'received_date', 'status']
    list_filter = ['branch', 'status', 'received_date']
    search_fields = ['grn_number', 'supplier__name']
    inlines = [GoodsReceiptItemInline]


@admin.register(PurchasePayment)
class PurchasePaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_reference', 'amount_paid', 'payment_method', 'payment_date']
    list_filter = ['payment_method', 'payment_date']
