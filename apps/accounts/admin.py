"""Django Admin customization for Accounts."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User, LoginHistory

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role', 'branch', 'is_locked', 'is_active', 'created_at')
    list_filter = ('role', 'branch', 'is_locked', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('DineFlow Roles & Tenancy', {'fields': ('role', 'restaurant', 'branch', 'phone_number', 'avatar')}),
        ('Security & Lockout', {'fields': ('failed_login_attempts', 'is_locked', 'locked_until', 'last_login_ip')}),
    )

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('attempted_email', 'status', 'ip_address', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('attempted_email', 'ip_address', 'user_agent')
    readonly_fields = ('user', 'attempted_email', 'ip_address', 'user_agent', 'status', 'timestamp')
