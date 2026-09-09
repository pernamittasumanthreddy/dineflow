"""Customers Django Admin."""
from django.contrib import admin
from apps.customers.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'total_visits', 'total_spent', 'last_visit_date')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-total_spent',)
