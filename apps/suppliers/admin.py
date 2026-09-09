"""Suppliers Django Admin."""
from django.contrib import admin
from apps.suppliers.models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'gstin', 'contact_person', 'phone', 'city', 'rating', 'outstanding_balance', 'is_active')
    search_fields = ('company_name', 'gstin', 'contact_person', 'phone')
    list_filter = ('city', 'payment_terms', 'is_active')
