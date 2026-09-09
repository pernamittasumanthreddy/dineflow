from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Restaurant


class CustomerTier(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='loyalty_tiers')
    name = models.CharField(max_length=50)  # e.g., Bronze, Silver, Gold, Platinum
    min_lifetime_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    points_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    benefits_description = models.TextField(blank=True)
    badge_color = models.CharField(max_length=20, default='#CD7F32')

    class Meta:
        db_table = 'df_customer_tiers'
        verbose_name = 'Customer Tier'
        verbose_name_plural = 'Customer Tiers'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'name'], name='unique_tier_name_per_restaurant'),
            CheckConstraint(condition=Q(min_lifetime_spend__gte=0), name='tier_min_spend_non_negative'),
            CheckConstraint(condition=Q(points_multiplier__gt=0), name='tier_multiplier_positive'),
        ]

    def __str__(self):
        return f"{self.name} Tier ({self.points_multiplier}x points)"


class LoyaltyAccount(BaseModel):
    customer = models.OneToOneField('customers.Customer', on_delete=models.CASCADE, related_name='loyalty_account')
    tier = models.ForeignKey(CustomerTier, on_delete=models.PROTECT, related_name='accounts')
    current_points = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    lifetime_earned_points = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    lifetime_redeemed_points = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    last_activity_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_loyalty_accounts'
        verbose_name = 'Loyalty Account'
        verbose_name_plural = 'Loyalty Accounts'
        constraints = [
            CheckConstraint(condition=Q(current_points__gte=0), name='loyalty_points_non_negative'),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.current_points} pts [{self.tier.name}]"


class LoyaltyTransaction(BaseModel):
    TRANSACTION_TYPES = [
        ('EARNED', 'Points Earned from Purchase'),
        ('REDEEMED', 'Points Redeemed on Bill'),
        ('BONUS', 'Bonus Points Credited'),
        ('EXPIRED', 'Points Expired'),
        ('ADJUSTMENT', 'Manual Adjustment'),
    ]

    account = models.ForeignKey(LoyaltyAccount, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='loyalty_transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, db_index=True)
    points = models.DecimalField(max_digits=10, decimal_places=2, help_text="+ for credit, - for debit")
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255)

    class Meta:
        db_table = 'df_loyalty_transactions'
        verbose_name = 'Loyalty Transaction'
        verbose_name_plural = 'Loyalty Transactions'
        ordering = ['-created_at']

    def __str__(self):
        sign = "+" if self.points > 0 else ""
        return f"{sign}{self.points} pts [{self.transaction_type}] - Balance: {self.balance_after}"


class Reward(BaseModel):
    REWARD_TYPES = [
        ('FREE_ITEM', 'Free Menu Item'),
        ('BILL_DISCOUNT', 'Bill Discount Voucher'),
        ('SPECIAL_PERK', 'Special Dining Perk'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='rewards')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    points_required = models.PositiveIntegerField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES, default='BILL_DISCOUNT')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_rewards'
        verbose_name = 'Loyalty Reward'
        verbose_name_plural = 'Loyalty Rewards'
        constraints = [
            CheckConstraint(condition=Q(points_required__gt=0), name='reward_points_positive'),
            CheckConstraint(condition=Q(discount_amount__gte=0), name='reward_discount_non_negative'),
        ]

    def __str__(self):
        return f"{self.title} ({self.points_required} pts)"


class RewardRedemption(BaseModel):
    account = models.ForeignKey(LoyaltyAccount, on_delete=models.CASCADE, related_name='redemptions')
    reward = models.ForeignKey(Reward, on_delete=models.PROTECT, related_name='redemptions')
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_redemptions'
    )
    points_spent = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('REDEEMED', 'Redeemed'), ('CANCELLED', 'Cancelled')],
        default='REDEEMED'
    )
    redeemed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_reward_redemptions'
        verbose_name = 'Reward Redemption'
        verbose_name_plural = 'Reward Redemptions'

    def __str__(self):
        return f"{self.account.customer.name} redeemed {self.reward.title} for {self.points_spent} pts"
