from django.contrib import admin
from .models import Notification, NotificationPreference, NotificationReadStatus


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'priority', 'branch', 'user', 'channel', 'created_at']
    list_filter = ['notification_type', 'priority', 'channel', 'created_at']
    search_fields = ['title', 'message']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'sms_notifications', 'push_notifications']


@admin.register(NotificationReadStatus)
class NotificationReadStatusAdmin(admin.ModelAdmin):
    list_display = ['notification', 'user', 'is_read', 'read_at']
