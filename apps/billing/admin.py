"""Billing Django Admin Registration."""
from django.contrib import admin
from apps.billing.models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ('item_name', 'sac_code', 'quantity', 'unit_rate', 'item_total', 'tax_rate_percent', 'cgst_amount', 'sgst_amount')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'branch', 'grand_total', 'cgst_amount', 'sgst_amount', 'is_paid', 'created_at')
    list_filter = ('branch', 'is_paid', 'created_at')
    search_fields = ('invoice_number', 'restaurant_gstin', 'customer__name', 'customer__phone')
    inlines = [InvoiceItemInline]
