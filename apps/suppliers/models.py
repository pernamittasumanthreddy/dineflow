"""Vendor Master, Regulatory GSTIN, and Procurement Terms Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Supplier(TimeStampedModel, SoftDeleteModel):
    """Vendor supplying raw provisions, poultry, dairy, produce, or beverages."""
    company_name = models.CharField('Supplier / Company Name', max_length=150, db_index=True)
    gstin = models.CharField('GSTIN', max_length=15, blank=True, help_text='15-digit GST Identification Number')
    fssai_number = models.CharField('FSSAI Lic #', max_length=20, blank=True)
    contact_person = models.CharField('Contact Person', max_length=100)
    phone = models.CharField('Phone Number', max_length=20)
    email = models.EmailField('Email Address', blank=True)
    address = models.TextField('Office / Warehouse Address')
    city = models.CharField(max_length=100, default='Hyderabad')
    state = models.CharField(max_length=100, default='Telangana')
    
    # Financial Terms
    payment_terms = models.CharField('Payment Terms', max_length=50, default='NET_15', help_text='e.g., ADVANCE, COD, NET_15, NET_30')
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField('IFSC Code', max_length=20, blank=True)
    
    # Performance & Balance
    outstanding_balance = models.DecimalField('Outstanding (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    rating = models.DecimalField('Performance Rating (1-5)', max_digits=3, decimal_places=1, default=Decimal('4.5'))
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Supplier / Vendor'
        verbose_name_plural = 'Suppliers & Vendors'
        ordering = ['company_name']

    def __str__(self):
        return f"{self.company_name} ({self.city}) - Rating: {self.rating}★"
