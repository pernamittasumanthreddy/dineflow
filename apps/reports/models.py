"""Generated Report Audit and Archive Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class GeneratedReportRecord(TimeStampedModel):
    """Audit log of generated and exported PDF / Excel compliance reports."""
    title = models.CharField(max_length=150)
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('SALES_PDF', 'Sales & Revenue Audit (PDF)'),
            ('GSTR1_EXCEL', 'Indian GSTR-1 Sales Return (Excel)'),
            ('INVENTORY_EXCEL', 'Stock Valuation & Low-Stock Ledger (Excel)'),
            ('PAYROLL_EXCEL', 'Monthly Payroll Register (Excel)'),
        ]
    )
    format = models.CharField(max_length=10, choices=[('PDF', 'PDF'), ('EXCEL', 'Excel'), ('CSV', 'CSV')])
    file_path = models.CharField(max_length=255, blank=True)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='generated_reports')

    class Meta:
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.format}) at {self.created_at}"
