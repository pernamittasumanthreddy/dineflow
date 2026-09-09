"""Delivery Django Admin."""
from django.contrib import admin
from apps.delivery.models import DeliveryOrder

@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'recipient_name', 'recipient_phone', 'assigned_rider', 'status', 'estimated_delivery_minutes', 'delivered_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'recipient_name', 'recipient_phone')
