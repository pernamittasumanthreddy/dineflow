from django.contrib import admin

from .models import Coupon, CouponUsage, Offer


class CouponInline(admin.TabularInline):
    model = Coupon
    extra = 1


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'restaurant', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['restaurant', 'discount_type', 'is_active']
    search_fields = ['title']
    inlines = [CouponInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'offer', 'times_used', 'is_active']
    search_fields = ['code']


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'customer', 'order', 'discount_availed', 'used_at']
    list_filter = ['used_at']
