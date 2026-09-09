"""Guest Ratings, Culinary Reviews, and Management Feedback Models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel

class Review(TimeStampedModel):
    """Guest feedback on dining experience, food quality, and staff hospitality."""
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='reviews')
    
    # Rating Scores (1-5)
    overall_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    food_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    ambience_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    service_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    
    comment = models.TextField('Customer Feedback')
    management_response = models.TextField('Restaurant Response', blank=True)
    responded_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='review_responses')
    responded_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField('Approved / Visible Publicly', default=True)

    class Meta:
        verbose_name = 'Customer Review'
        verbose_name_plural = 'Customer Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.name} - {self.overall_rating}★ for {self.branch.name}"
