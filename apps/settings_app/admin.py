from django.contrib import admin

from .models import (
    BackupRecord,
    BranchSetting,
    NotificationSetting,
    RestaurantSetting,
    SystemSetting,
)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_type', 'is_encrypted']
    search_fields = ['key']


@admin.register(RestaurantSetting)
class RestaurantSettingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'key', 'value']
    list_filter = ['restaurant']


@admin.register(BranchSetting)
class BranchSettingAdmin(admin.ModelAdmin):
    list_display = ['branch', 'key', 'value']
    list_filter = ['branch']


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['branch', 'email_host', 'sms_sender_id', 'is_sms_active']


@admin.register(BackupRecord)
class BackupRecordAdmin(admin.ModelAdmin):
    list_display = ['backup_id', 'backup_type', 'status', 'file_size_bytes', 'created_at', 'restore_status']
    list_filter = ['backup_type', 'status', 'restore_status']
    readonly_fields = ['backup_id', 'file_path', 'file_size_bytes', 'checksum_sha256', 'created_at']
