"""Employees Django Admin."""
from django.contrib import admin
from apps.employees.models import Department, Designation, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department')
    list_filter = ('department',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'branch', 'department', 'designation', 'basic_salary', 'is_active')
    list_filter = ('branch', 'department', 'designation', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email', 'pan_number')
