"""Audit Django Admin."""
from django.contrib import admin
from apps.audit.models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'module_name', 'object_repr', 'ip_address')
    list_filter = ('action', 'module_name', 'timestamp')
    search_fields = ('object_repr', 'actor__email')
    readonly_fields = ('actor', 'action', 'module_name', 'object_id', 'object_repr', 'ip_address', 'old_values', 'new_values', 'timestamp')
