"""Refunds Django Admin."""
from django.contrib import admin
from apps.refunds.models import RefundRequest

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('refund_number', 'order', 'amount', 'status', 'requested_by', 'approved_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('refund_number', 'order__order_number', 'reason')
