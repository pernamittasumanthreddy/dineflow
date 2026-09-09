"""Multi-Branch Hierarchy and Local Outlet Models."""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Branch(TimeStampedModel, SoftDeleteModel):
    """Specific outlet/location of a Restaurant enterprise."""
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='branches'
    )
    name = models.CharField('Branch Name', max_length=150)
    code = models.CharField('Branch Code', max_length=20, unique=True, help_text='Short alphanumeric outlet code')
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches'
    )
    phone = models.CharField('Contact Phone', max_length=20)
    email = models.EmailField('Branch Email', blank=True)
    
    # Location
    address = models.TextField('Physical Address')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Operations
    opening_time = models.TimeField(default='11:00')
    closing_time = models.TimeField(default='23:00')
    total_seating_capacity = models.PositiveIntegerField(default=60)
    
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.city}"
