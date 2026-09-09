from django.contrib import admin

from .models import Review, ReviewModeration, ReviewResponse


class ReviewResponseInline(admin.StackedInline):
    model = ReviewResponse
    extra = 0


class ReviewModerationInline(admin.StackedInline):
    model = ReviewModeration
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'branch', 'overall_rating', 'food_rating', 'service_rating', 'is_public', 'created_at']
    list_filter = ['branch', 'overall_rating', 'is_public']
    search_fields = ['customer__name', 'comment']
    inlines = [ReviewResponseInline, ReviewModerationInline]
