from django.contrib import admin

from .models import AuditLog, LoginHistory, SecurityEvent


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'model_name', 'object_repr', 'user', 'branch', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['model_name', 'object_repr', 'user__email']
    readonly_fields = ['action', 'model_name', 'object_id', 'object_repr', 'user', 'branch', 'ip_address', 'user_agent', 'changes', 'timestamp']


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'severity', 'user', 'ip_address', 'timestamp']
    list_filter = ['event_type', 'severity', 'timestamp']


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ip_address', 'login_time', 'logout_time']
    list_filter = ['status', 'login_time']
