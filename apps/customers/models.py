"""Guest CRM, Dining Preferences, and Lifetime Analytics Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Customer(TimeStampedModel, SoftDeleteModel):
    """Customer CRM entity tracking dining visits, preferences, and lifetime value."""
    name = models.CharField('Customer Name', max_length=150, db_index=True)
    phone = models.CharField('Phone Number', max_length=20, unique=True, db_index=True)
    email = models.EmailField('Email Address', blank=True, null=True)
    address = models.TextField('Address', blank=True)
    city = models.CharField(max_length=100, default='Hyderabad')
    
    # Dining preferences
    dietary_preferences = models.CharField(max_length=100, blank=True, help_text='e.g., Pure Veg, Jain, Low Spice, Gluten-Free')
    special_notes = models.TextField('Guest Notes / Anniversary / Allergies', blank=True)
    
    # Aggregated metrics
    total_visits = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    last_visit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"
