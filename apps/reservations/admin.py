"""Reservations Django Admin."""
from django.contrib import admin
from apps.reservations.models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'guest_phone', 'reservation_date', 'reservation_time', 'guest_count', 'assigned_table', 'status')
    list_filter = ('branch', 'status', 'reservation_date')
    search_fields = ('guest_name', 'guest_phone', 'guest_email')
    list_editable = ('status',)
