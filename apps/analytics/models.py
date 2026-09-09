"""Executive KPI Snapshot and Restaurant Business Intelligence Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class DailyAnalyticsSnapshot(TimeStampedModel):
    """Aggregated daily restaurant performance record for business intelligence."""
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='analytics_snapshots')
    date = models.DateField(db_index=True)
    
    # Financial KPIs
    total_revenue = models.DecimalField('Gross Revenue (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_expenses = models.DecimalField('Total Expenses (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    net_profit = models.DecimalField('Net Profit (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Operational KPIs
    order_count = models.PositiveIntegerField('Total Orders', default=0)
    guest_covers = models.PositiveIntegerField('Total Guests Served', default=0)
    average_order_value = models.DecimalField('AOV (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Hospitality Efficiency
    revpash = models.DecimalField('RevPASH (₹/Seat-Hour)', max_digits=8, decimal_places=2, default=Decimal('0.00'))
    table_turnover_rate = models.DecimalField('Table Turnover Rate', max_digits=5, decimal_places=2, default=Decimal('0.00'))
    food_cost_percentage = models.DecimalField('Food Cost (COGS) %', max_digits=5, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Daily Analytics Snapshot'
        verbose_name_plural = 'Daily Analytics Snapshots'
        unique_together = ('branch', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Analytics {self.branch.code} on {self.date}: ₹{self.total_revenue} (RevPASH: ₹{self.revpash})"
