from django.contrib import admin
from .models import (
    InvoiceNumberSequence, Invoice, InvoiceItem,
    InvoiceTax, InvoiceDiscount
)


@admin.register(InvoiceNumberSequence)
class InvoiceNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ['branch', 'fiscal_year', 'prefix', 'last_number', 'updated_at']
    list_filter = ['branch', 'fiscal_year']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


class InvoiceTaxInline(admin.TabularInline):
    model = InvoiceTax
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'branch', 'grand_total', 'status', 'invoice_date']
    list_filter = ['branch', 'status', 'invoice_date']
    search_fields = ['invoice_number', 'customer_name', 'customer_phone']
    inlines = [InvoiceItemInline, InvoiceTaxInline]
