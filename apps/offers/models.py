from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant


class Offer(BaseModel):
    DISCOUNT_TYPES = [
        ('PERCENTAGE', 'Percentage Discount'),
        ('FLAT', 'Flat Amount Discount'),
        ('BOGO', 'Buy One Get One Free'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='PERCENTAGE')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit_total = models.PositiveIntegerField(null=True, blank=True)
    usage_limit_per_customer = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_offers'
        verbose_name = 'Offer / Promotion'
        verbose_name_plural = 'Offers / Promotions'
        constraints = [
            CheckConstraint(condition=Q(discount_value__gte=0), name='offer_discount_val_non_negative'),
            CheckConstraint(condition=Q(min_order_value__gte=0), name='offer_min_order_non_negative'),
            CheckConstraint(condition=Q(valid_to__gte=models.F('valid_from')), name='offer_validity_window'),
        ]

    def __str__(self):
        return f"{self.title} ({self.discount_value} {self.discount_type})"


class Coupon(BaseModel):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=50, unique=True, db_index=True)
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return f"{self.code} ({self.offer.title})"


class CouponUsage(BaseModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='coupon_usages')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='coupon_usages')
    discount_availed = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_coupon_usages'
        verbose_name = 'Coupon Usage'
        verbose_name_plural = 'Coupon Usages'
        constraints = [
            CheckConstraint(condition=Q(discount_availed__gte=0), name='coupon_discount_availed_non_negative')
        ]

    def __str__(self):
        return f"{self.coupon.code} used by {self.customer.name} (₹{self.discount_availed})"


class OfferMenuItem(BaseModel):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='targeted_items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, related_name='applicable_offers')

    class Meta:
        db_table = 'df_offer_menu_items'
        verbose_name = 'Offer Menu Item'
        verbose_name_plural = 'Offer Menu Items'
        constraints = [
            models.UniqueConstraint(fields=['offer', 'menu_item'], name='unique_offer_menu_item')
        ]

    def __str__(self):
        return f"{self.offer.title} -> {self.menu_item.name}"


class OfferBranch(BaseModel):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='applicable_branches')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_offers')

    class Meta:
        db_table = 'df_offer_branches'
        verbose_name = 'Offer Branch'
        verbose_name_plural = 'Offer Branches'
        constraints = [
            models.UniqueConstraint(fields=['offer', 'branch'], name='unique_offer_branch')
        ]

    def __str__(self):
        return f"{self.offer.title} -> {self.branch.name}"
