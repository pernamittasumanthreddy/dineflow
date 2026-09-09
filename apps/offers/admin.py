"""Offers Django Admin."""
from django.contrib import admin
from apps.offers.models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'discount_type', 'discount_value', 'min_order_amount', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code', 'title')
