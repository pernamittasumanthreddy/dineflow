"""Shifts Django Admin."""
from django.contrib import admin
from apps.shifts.models import Shift, ShiftRoster

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'break_duration_minutes')

@admin.register(ShiftRoster)
class ShiftRosterAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift', 'date', 'status')
    list_filter = ('shift', 'date', 'status')
    search_fields = ('employee__employee_id', 'employee__user__first_name')
