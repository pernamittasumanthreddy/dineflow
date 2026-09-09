from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class Review(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='reviews')
    order = models.OneToOneField(
        'orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='review'
    )
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='reviews')
    food_rating = models.PositiveSmallIntegerField()
    service_rating = models.PositiveSmallIntegerField()
    ambiance_rating = models.PositiveSmallIntegerField()
    overall_rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    is_public = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'df_reviews'
        verbose_name = 'Customer Review'
        verbose_name_plural = 'Customer Reviews'
        constraints = [
            CheckConstraint(condition=Q(food_rating__gte=1) & Q(food_rating__lte=5), name='review_food_rating_range'),
            CheckConstraint(condition=Q(service_rating__gte=1) & Q(service_rating__lte=5), name='review_service_rating_range'),
            CheckConstraint(condition=Q(ambiance_rating__gte=1) & Q(ambiance_rating__lte=5), name='review_ambiance_rating_range'),
            CheckConstraint(condition=Q(overall_rating__gte=1) & Q(overall_rating__lte=5), name='review_overall_rating_range'),
        ]
        indexes = [
            models.Index(fields=['branch', 'overall_rating']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.overall_rating}★ for {self.branch.name}"


class ReviewResponse(BaseModel):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    response_text = models.TextField()
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    responded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_review_responses'
        verbose_name = 'Review Response'
        verbose_name_plural = 'Review Responses'

    def __str__(self):
        return f"Response to Review #{self.review.id}"


class ReviewModeration(BaseModel):
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged for Review'),
        ('HIDDEN', 'Hidden'),
        ('SPAM', 'Spam'),
    ]

    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='moderation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    moderation_reason = models.TextField(blank=True)
    moderated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_review_moderations'
        verbose_name = 'Review Moderation'
        verbose_name_plural = 'Review Moderations'

    def __str__(self):
        return f"Moderation for Review #{self.review.id}: {self.status}"
