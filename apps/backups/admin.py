"""Backups Django Admin."""
from django.contrib import admin
from apps.backups.models import DatabaseBackupRecord

@admin.register(DatabaseBackupRecord)
class DatabaseBackupRecordAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file_size_bytes', 'status', 'created_at')
    readonly_fields = ('filename', 'file_path', 'file_size_bytes', 'status', 'created_at')
