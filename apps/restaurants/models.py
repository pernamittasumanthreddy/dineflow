"""Restaurant Profile and Enterprise Business Models."""
from django.db import models

class Restaurant(models.Model):
    """Central Restaurant Corporate Entity supporting multi-branch operations."""
    name = models.CharField('Restaurant Name', max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    legal_entity_name = models.CharField('Legal Entity Name', max_length=200, blank=True)
    
    # Indian Regulatory Identifiers
    gstin = models.CharField('GSTIN', max_length=15, help_text='15-digit Indian GST Identification Number')
    fssai_number = models.CharField('FSSAI License No.', max_length=14, help_text='14-digit FSSAI License Number')
    
    # Contact & Location
    email = models.EmailField('Contact Email')
    phone = models.CharField('Phone Number', max_length=20)
    website = models.URLField(blank=True, null=True)
    address_line1 = models.CharField('Address Line 1', max_length=255)
    address_line2 = models.CharField('Address Line 2', max_length=255, blank=True)
    city = models.CharField('City', max_length=100, default='Hyderabad')
    state = models.CharField('State', max_length=100, default='Telangana')
    pincode = models.CharField('PIN Code', max_length=10, default='500034')
    country = models.CharField('Country', max_length=50, default='India')
    
    # Regional Configurations
    currency = models.CharField('Currency', max_length=10, default='INR')
    currency_symbol = models.CharField('Currency Symbol', max_length=5, default='₹')
    timezone = models.CharField('Timezone', max_length=50, default='Asia/Kolkata')
    
    # Brand Assets
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    
    # Operational Hours
    opening_time = models.TimeField(default='10:00')
    closing_time = models.TimeField(default='23:30')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f"{self.name} (GSTIN: {self.gstin})"


class RestaurantSetting(models.Model):
    """Operational parameters, default tax configurations, and system switches."""
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='settings')
    default_cgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)
    default_sgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=2.50)
    default_service_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_tax_inclusive = models.BooleanField('Tax-Inclusive Pricing', default=False)
    
    invoice_prefix = models.CharField(max_length=10, default='INV')
    bill_footer_message = models.TextField(default='Thank you for dining with us! FSSAI Lic: Certified.')
    enable_table_reservations = models.BooleanField(default=True)
    enable_kds = models.BooleanField(default=True)
    enable_delivery_dispatch = models.BooleanField(default=True)
    low_stock_alert_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.restaurant.name}"
