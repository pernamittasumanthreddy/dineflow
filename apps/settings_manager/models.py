"""Global Tenant Switches and Hardware Peripheral Print Settings Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class SystemSetting(TimeStampedModel):
    """Global ERP configuration keys and thermal printer hardware switches."""
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
        ordering = ['key']

    def __str__(self):
        return f"{self.key} = {self.value}"
