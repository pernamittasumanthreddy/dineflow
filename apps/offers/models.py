"""Promotional Offers, Coupons, and Bill Discount Models."""
from django.db import models
from decimal import Decimal
from django.utils import timezone
from apps.core.models import TimeStampedModel, SoftDeleteModel

class DiscountType(models.TextChoices):
    PERCENTAGE = 'PERCENTAGE', 'Percentage (%) Off'
    FLAT = 'FLAT', 'Flat (₹) Amount Off'

class Offer(TimeStampedModel, SoftDeleteModel):
    """Marketing promotion or coupon code applied at POS checkout."""
    code = models.CharField('Coupon Code', max_length=50, unique=True, db_index=True)
    title = models.CharField('Offer Title', max_length=150)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='offers',
        help_text='Leave empty for all branches'
    )
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices, default=DiscountType.PERCENTAGE)
    discount_value = models.DecimalField('Discount Value (% or ₹)', max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField('Min Order Value (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    max_discount_amount = models.DecimalField('Max Cap (₹)', max_digits=10, decimal_places=2, null=True, blank=True)
    
    valid_from = models.DateTimeField('Valid From', default=timezone.now)
    valid_to = models.DateTimeField('Valid Until')
    usage_limit = models.PositiveIntegerField('Max Total Redemptions', default=1000)
    times_used = models.PositiveIntegerField('Times Redeemed', default=0)

    class Meta:
        verbose_name = 'Offer / Coupon'
        verbose_name_plural = 'Offers & Coupons'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.title} ({self.discount_value}{'%' if self.discount_type == DiscountType.PERCENTAGE else '₹'} Off)"

    @property
    def is_valid_now(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to and self.times_used < self.usage_limit
