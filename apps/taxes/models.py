from django.db import models
from django.db.models import Q, CheckConstraint
from apps.core.models import BaseModel, Restaurant, Branch


class TaxCategory(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tax_categories')
    name = models.CharField(max_length=100)  # e.g., "Restaurant Dining (5% GST)", "Packaged Beverages (12% GST)"
    code = models.CharField(max_length=50)
    hsn_sac_code = models.CharField(max_length=10, default='996331')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_tax_categories'
        verbose_name = 'Tax Category'
        verbose_name_plural = 'Tax Categories'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'code'], name='unique_tax_category_per_restaurant')
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class TaxRate(BaseModel):
    COMPONENT_CHOICES = [
        ('CGST', 'Central GST'),
        ('SGST', 'State GST'),
        ('IGST', 'Integrated GST'),
        ('VAT', 'Value Added Tax (Liquor)'),
        ('CESS', 'GST Compensation Cess'),
    ]

    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE, related_name='rates')
    component_name = models.CharField(max_length=20, choices=COMPONENT_CHOICES)
    rate_percent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_tax_rates'
        verbose_name = 'Tax Rate'
        verbose_name_plural = 'Tax Rates'
        constraints = [
            CheckConstraint(
                condition=Q(rate_percent__gte=0) & Q(rate_percent__lte=100),
                name='tax_rate_valid_percentage'
            )
        ]

    def __str__(self):
        return f"{self.component_name} - {self.rate_percent}% ({self.tax_category.name})"


class TaxRule(BaseModel):
    RULE_TYPES = [
        ('INTRA_STATE', 'Intra-State (CGST + SGST)'),
        ('INTER_STATE', 'Inter-State (IGST)'),
    ]

    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE, related_name='rules')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES, default='INTRA_STATE')
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'df_tax_rules'
        verbose_name = 'Tax Rule'
        verbose_name_plural = 'Tax Rules'

    def __str__(self):
        return f"{self.tax_category.name} [{self.rule_type}]"


class RestaurantTaxConfiguration(BaseModel):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='tax_configuration')
    pan_number = models.CharField(max_length=10)
    is_composition_scheme = models.BooleanField(default=False)
    default_service_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_restaurant_tax_configs'
        verbose_name = 'Restaurant Tax Configuration'
        verbose_name_plural = 'Restaurant Tax Configurations'

    def __str__(self):
        return f"Tax Config for {self.restaurant.name}"


class BranchTaxConfiguration(BaseModel):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='tax_configuration')
    gstin = models.CharField(max_length=15, help_text="State-specific GSTIN")
    state_code = models.CharField(max_length=2, help_text="2-digit state code: 36=TS, 37=AP, 29=KA, 33=TN, 32=KL")
    is_sez = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_branch_tax_configs'
        verbose_name = 'Branch Tax Configuration'
        verbose_name_plural = 'Branch Tax Configurations'

    def __str__(self):
        return f"GSTIN: {self.gstin} ({self.branch.name})"
