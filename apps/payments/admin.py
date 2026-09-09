"""Payments Django Admin."""
from django.contrib import admin
from apps.payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_reference', 'order', 'amount', 'payment_method', 'status', 'cashier', 'payment_date')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('transaction_reference', 'order__order_number', 'upi_vpa')
