"""Loyalty Django Admin."""
from django.contrib import admin
from apps.loyalty.models import LoyaltyAccount, LoyaltyTransaction

class LoyaltyTransactionInline(admin.TabularInline):
    model = LoyaltyTransaction
    extra = 0
    readonly_fields = ('points', 'transaction_type', 'description', 'created_at')

@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = ('customer', 'points_balance', 'current_tier', 'lifetime_points')
    list_filter = ('current_tier',)
    search_fields = ('customer__name', 'customer__phone')
    inlines = [LoyaltyTransactionInline]
