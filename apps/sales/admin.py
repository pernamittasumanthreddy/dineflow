"""Sales Django Admin."""
from django.contrib import admin
from apps.sales.models import CashRegisterSession, ZReport

@admin.register(CashRegisterSession)
class CashRegisterSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'opened_by', 'opening_cash', 'closing_cash', 'cash_discrepancy', 'status', 'opened_at')
    list_filter = ('branch', 'status', 'opened_at')

@admin.register(ZReport)
class ZReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'branch', 'total_orders', 'gross_sales', 'net_sales', 'cash_sales', 'upi_sales', 'generated_by')
    list_filter = ('branch', 'report_date')
