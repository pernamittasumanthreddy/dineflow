from django.contrib import admin

from .models import (
    Reservation,
    ReservationGuest,
    RestaurantTable,
    TableAssignment,
    TableSection,
)


@admin.register(TableSection)
class TableSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'floor', 'is_active']
    list_filter = ['branch', 'is_active']


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'branch', 'section', 'seating_capacity', 'status', 'is_active']
    list_filter = ['branch', 'section', 'status', 'is_active']
    search_fields = ['table_number']


class ReservationGuestInline(admin.TabularInline):
    model = ReservationGuest
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'branch', 'customer', 'reservation_time', 'party_size', 'status']
    list_filter = ['branch', 'status', 'reservation_time']
    search_fields = ['reservation_number', 'customer__name', 'customer__phone']
    inlines = [ReservationGuestInline]


@admin.register(TableAssignment)
class TableAssignmentAdmin(admin.ModelAdmin):
    list_display = ['table', 'waiter', 'reservation', 'assigned_at', 'status']
    list_filter = ['status', 'assigned_at']
