"""Payroll Django Admin."""
from django.contrib import admin
from apps.payroll.models import Payroll

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'gross_earnings', 'total_deductions', 'net_salary', 'status', 'disbursed_at')
    list_filter = ('month', 'year', 'status')
    search_fields = ('employee__employee_id', 'employee__user__first_name', 'payment_reference')
