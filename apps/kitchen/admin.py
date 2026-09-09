"""Kitchen Django Admin Registration."""
from django.contrib import admin
from apps.kitchen.models import KitchenTicket

@admin.register(KitchenTicket)
class KitchenTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'order', 'station', 'status', 'expected_prep_minutes', 'elapsed_minutes', 'is_delayed', 'created_at')
    list_filter = ('station', 'status', 'created_at')
    search_fields = ('ticket_number', 'order__order_number')
