from django.contrib import admin

from .models import (
    DeliveryAddress,
    DeliveryAssignment,
    DeliveryOrder,
    DeliveryStatusHistory,
)


class DeliveryAddressInline(admin.StackedInline):
    model = DeliveryAddress
    can_delete = False


class DeliveryAssignmentInline(admin.TabularInline):
    model = DeliveryAssignment
    extra = 0


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'branch', 'customer', 'delivery_channel', 'status', 'estimated_delivery_time_minutes']
    list_filter = ['branch', 'status', 'delivery_channel']
    inlines = [DeliveryAddressInline, DeliveryAssignmentInline]


@admin.register(DeliveryStatusHistory)
class DeliveryStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['delivery_order', 'old_status', 'new_status', 'timestamp']
    list_filter = ['new_status', 'timestamp']
