"""Reviews Django Admin."""
from django.contrib import admin
from apps.reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'branch', 'overall_rating', 'food_rating', 'service_rating', 'is_published', 'created_at')
    list_filter = ('overall_rating', 'is_published', 'created_at')
    search_fields = ('customer__name', 'comment')
