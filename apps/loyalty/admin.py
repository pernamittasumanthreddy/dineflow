from django.contrib import admin

from .models import (
    CustomerTier,
    LoyaltyAccount,
    LoyaltyTransaction,
    Reward,
    RewardRedemption,
)


@admin.register(CustomerTier)
class CustomerTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'min_lifetime_spend', 'points_multiplier']


class LoyaltyTransactionInline(admin.TabularInline):
    model = LoyaltyTransaction
    extra = 0
    readonly_fields = ['transaction_type', 'points', 'balance_before', 'balance_after', 'reason', 'created_at']


@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = ['customer', 'tier', 'current_points', 'lifetime_earned_points', 'lifetime_redeemed_points']
    search_fields = ['customer__name', 'customer__phone']
    inlines = [LoyaltyTransactionInline]


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['title', 'restaurant', 'points_required', 'reward_type', 'discount_amount', 'is_active']
    list_filter = ['restaurant', 'reward_type', 'is_active']


@admin.register(RewardRedemption)
class RewardRedemptionAdmin(admin.ModelAdmin):
    list_display = ['account', 'reward', 'points_spent', 'status', 'redeemed_at']
    list_filter = ['status', 'redeemed_at']
