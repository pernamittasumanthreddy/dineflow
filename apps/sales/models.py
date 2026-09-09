"""Daily Cash Drawer Sessions, Register Reconciliation, and Statutory Z-Reports Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class CashRegisterSession(TimeStampedModel):
    """Daily shift drawer opening and closing cash reconciliation."""
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='register_sessions')
    opened_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='opened_registers')
    opening_cash = models.DecimalField('Opening Float Cash (₹)', max_digits=12, decimal_places=2, default=Decimal('2000.00'))
    
    closed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='closed_registers')
    closing_cash = models.DecimalField('Counted Cash (₹)', max_digits=12, decimal_places=2, null=True, blank=True)
    expected_cash = models.DecimalField('Expected Cash (₹)', max_digits=12, decimal_places=2, null=True, blank=True)
    cash_discrepancy = models.DecimalField('Difference / Shortage (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], default='OPEN', db_index=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Cash Drawer Session'
        verbose_name_plural = 'Cash Drawer Sessions'
        ordering = ['-opened_at']

    def __str__(self):
        return f"Register #{self.id} ({self.branch.name}) - [{self.status}]"

class ZReport(TimeStampedModel):
    """Statutory end-of-day register closure (Z-Report)."""
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='z_reports')
    report_date = models.DateField('Audit Date', db_index=True)
    
    # Sales Aggregates
    total_orders = models.PositiveIntegerField(default=0)
    gross_sales = models.DecimalField('Gross Sales (₹)', max_digits=12, decimal_places=2)
    discount_total = models.DecimalField('Discounts Given (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_total = models.DecimalField('GST Tax Collected (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_sales = models.DecimalField('Net Revenue (₹)', max_digits=12, decimal_places=2)
    
    # Method Splits
    cash_sales = models.DecimalField('Cash Sales (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    card_sales = models.DecimalField('Card Sales (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    upi_sales = models.DecimalField('UPI Sales (₹)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Expenses & Final Balance
    total_expenses = models.DecimalField('Cash Outflow / Expenses (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_drawer_balance = models.DecimalField('Net Drawer Cash (₹)', max_digits=12, decimal_places=2)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='generated_z_reports')

    class Meta:
        verbose_name = 'Daily Z-Report'
        verbose_name_plural = 'Daily Z-Reports'
        unique_together = ('branch', 'report_date')
        ordering = ['-report_date']

    def __str__(self):
        return f"Z-Report {self.branch.code} on {self.report_date}: Net ₹{self.net_sales}"
