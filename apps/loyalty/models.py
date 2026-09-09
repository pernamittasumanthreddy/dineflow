"""Guest Loyalty Points, Tier Engine, and Rewards Ledger Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class LoyaltyTier(models.TextChoices):
    BRONZE = 'BRONZE', 'Bronze (1x Points)'
    SILVER = 'SILVER', 'Silver (1.25x Points)'
    GOLD = 'GOLD', 'Gold (1.5x Points)'
    PLATINUM = 'PLATINUM', 'Platinum (2x Points)'

class LoyaltyAccount(TimeStampedModel):
    """Customer reward balance and VIP tier tracking."""
    customer = models.OneToOneField('customers.Customer', on_delete=models.CASCADE, related_name='loyalty_account')
    points_balance = models.PositiveIntegerField('Available Points', default=0)
    lifetime_points = models.PositiveIntegerField('Lifetime Earned Points', default=0)
    current_tier = models.CharField(max_length=20, choices=LoyaltyTier.choices, default=LoyaltyTier.BRONZE)

    class Meta:
        verbose_name = 'Loyalty Account'
        verbose_name_plural = 'Loyalty Accounts'

    def __str__(self):
        return f"{self.customer.name} - {self.points_balance} pts [{self.get_current_tier_display()}]"

    def update_tier(self):
        """Tier progression based on lifetime points."""
        if self.lifetime_points >= 5000:
            self.current_tier = LoyaltyTier.PLATINUM
        elif self.lifetime_points >= 2500:
            self.current_tier = LoyaltyTier.GOLD
        elif self.lifetime_points >= 1000:
            self.current_tier = LoyaltyTier.SILVER
        else:
            self.current_tier = LoyaltyTier.BRONZE
        self.save(update_fields=['current_tier'])

class LoyaltyTransaction(TimeStampedModel):
    """Immutable ledger of points earned and redeemed."""
    account = models.ForeignKey(LoyaltyAccount, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='loyalty_transactions')
    points = models.IntegerField('Points Delta (+ for earn, - for burn)')
    transaction_type = models.CharField(
        max_length=20,
        choices=[('EARNED', 'Points Earned'), ('REDEEMED', 'Points Redeemed'), ('EXPIRED', 'Points Expired'), ('BONUS', 'Bonus Points')]
    )
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Loyalty Transaction'
        verbose_name_plural = 'Loyalty Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account.customer.name}: {self.points:+d} pts ({self.transaction_type})"
