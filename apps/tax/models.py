"""Indian GST Regulatory Tax Engine and Slabs Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class TaxCategory(TimeStampedModel):
    """GST tax categories (Food 5%, Alcoholic Beverages 18%, Exempt, etc.)."""
    name = models.CharField(max_length=100)
    sac_code = models.CharField('SAC / HSN Code', max_length=20, default='996331', help_text='SAC 9963 for Restaurant Services')
    total_rate_percent = models.DecimalField('Total GST Rate %', max_digits=5, decimal_places=2, default=Decimal('5.00'))
    cgst_rate_percent = models.DecimalField('CGST Rate %', max_digits=5, decimal_places=2, default=Decimal('2.50'))
    sgst_rate_percent = models.DecimalField('SGST Rate %', max_digits=5, decimal_places=2, default=Decimal('2.50'))
    igst_rate_percent = models.DecimalField('IGST Rate %', max_digits=5, decimal_places=2, default=Decimal('5.00'))
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Tax Category'
        verbose_name_plural = 'Tax Categories'

    def __str__(self):
        return f"{self.name} ({self.total_rate_percent}% GST - SAC: {self.sac_code})"

    def save(self, *args, **kwargs):
        # Ensure automatic split between CGST and SGST for standard intra-state
        if not self.cgst_rate_percent or not self.sgst_rate_percent:
            half = self.total_rate_percent / Decimal('2.0')
            self.cgst_rate_percent = half
            self.sgst_rate_percent = half
        self.igst_rate_percent = self.total_rate_percent
        super().save(*args, **kwargs)
