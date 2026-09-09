"""Attendance Django Admin."""
from django.contrib import admin
from apps.attendance.models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status', 'late_minutes', 'overtime_hours')
    list_filter = ('date', 'status')
    search_fields = ('employee__employee_id', 'employee__user__first_name')
