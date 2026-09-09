from django.contrib import admin
from .models import (
    Customer, CustomerAddress, CustomerPreference,
    CustomerOrderHistory, CustomerReservationHistory
)


class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0


class CustomerPreferenceInline(admin.StackedInline):
    model = CustomerPreference
    can_delete = False


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'restaurant', 'total_visits', 'total_spend', 'loyalty_points', 'status']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['restaurant', 'status']
    inlines = [CustomerPreferenceInline, CustomerAddressInline]


@admin.register(CustomerOrderHistory)
class CustomerOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'order_amount', 'order_type']
    list_filter = ['order_type', 'order_date']


@admin.register(CustomerReservationHistory)
class CustomerReservationHistoryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'reservation_date', 'party_size', 'status']
