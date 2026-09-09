from django.contrib import admin

from .models import (
    Supplier,
    SupplierContact,
    SupplierPayment,
    SupplierProduct,
    SupplierRating,
)


class SupplierContactInline(admin.TabularInline):
    model = SupplierContact
    extra = 1


class SupplierProductInline(admin.TabularInline):
    model = SupplierProduct
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier_code', 'restaurant', 'contact_person', 'phone', 'city', 'is_active']
    list_filter = ['restaurant', 'city', 'is_active']
    search_fields = ['name', 'supplier_code', 'phone', 'gstin']
    inlines = [SupplierContactInline, SupplierProductInline]


@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'branch', 'amount', 'payment_date', 'payment_method', 'reference_number']
    list_filter = ['payment_method', 'payment_date', 'branch']


@admin.register(SupplierRating)
class SupplierRatingAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'quality_rating', 'delivery_punctuality_rating', 'pricing_rating', 'rating_date']
