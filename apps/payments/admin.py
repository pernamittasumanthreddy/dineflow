from django.contrib import admin
from .models import (
    PaymentMethod, Payment, PaymentTransaction,
    RefundReason, Refund
)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch', 'amount', 'payment_method', 'status', 'transaction_reference', 'paid_at']
    list_filter = ['branch', 'payment_method', 'status', 'paid_at']
    search_fields = ['transaction_reference', 'order__order_number', 'invoice__invoice_number']
    inlines = [PaymentTransactionInline]


@admin.register(RefundReason)
class RefundReasonAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'is_active']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['refund_number', 'amount', 'reason', 'refund_mode', 'refunded_at']
    list_filter = ['reason', 'refund_mode', 'refunded_at']
