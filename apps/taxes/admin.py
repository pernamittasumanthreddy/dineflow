from django.contrib import admin
from .models import (
    TaxCategory, TaxRate, TaxRule,
    RestaurantTaxConfiguration, BranchTaxConfiguration
)


class TaxRateInline(admin.TabularInline):
    model = TaxRate
    extra = 1


@admin.register(TaxCategory)
class TaxCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'restaurant', 'hsn_sac_code', 'is_active']
    list_filter = ['restaurant', 'is_active']
    inlines = [TaxRateInline]


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['component_name', 'rate_percent', 'tax_category', 'is_active']
    list_filter = ['component_name', 'is_active']


@admin.register(RestaurantTaxConfiguration)
class RestaurantTaxConfigurationAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'pan_number', 'is_composition_scheme', 'default_service_charge_percent']


@admin.register(BranchTaxConfiguration)
class BranchTaxConfigurationAdmin(admin.ModelAdmin):
    list_display = ['branch', 'gstin', 'state_code', 'is_sez']
