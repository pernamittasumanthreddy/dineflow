from django.contrib import admin
from .models import (
    Department, Designation, Employee, Shift, ShiftAssignment,
    Attendance, LeaveType, Leave, SalaryStructure, Payroll, PayrollItem
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'restaurant', 'branch', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'department', 'level']
    search_fields = ['title', 'code']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_code', 'user', 'branch', 'department', 'designation', 'status', 'date_of_joining']
    search_fields = ['employee_code', 'user__first_name', 'user__last_name', 'user__email', 'user__phone']
    list_filter = ['status', 'employment_type', 'department', 'branch']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'branch', 'date', 'check_in_time', 'check_out_time', 'status']
    list_filter = ['status', 'branch', 'date']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'start_time', 'end_time']


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status']
    list_filter = ['status', 'leave_type']


class PayrollItemInline(admin.TabularInline):
    model = PayrollItem
    extra = 0


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['branch', 'month', 'year', 'total_gross', 'total_net', 'status']
    list_filter = ['status', 'year', 'month', 'branch']
    inlines = [PayrollItemInline]
