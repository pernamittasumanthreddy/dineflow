"""Tax Django Admin."""
from django.contrib import admin
from apps.tax.models import TaxCategory

@admin.register(TaxCategory)
class TaxCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sac_code', 'total_rate_percent', 'cgst_rate_percent', 'sgst_rate_percent', 'is_active')
    list_editable = ('total_rate_percent', 'is_active')
