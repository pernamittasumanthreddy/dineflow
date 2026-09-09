"""Settings Manager Django Admin."""
from django.contrib import admin
from apps.settings_manager.models import SystemSetting

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'is_public')
    search_fields = ('key', 'value')
