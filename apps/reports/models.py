from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel, Branch, User


class ReportDefinition(BaseModel):
    REPORT_CATEGORIES = [
        ('TAXATION', 'Taxation & GST (GSTR-1, GSTR-3B)'),
        ('FINANCE', 'Finance & P&L'),
        ('OPERATIONS', 'Operations & Sales'),
        ('INVENTORY', 'Inventory & Costing'),
        ('HR', 'HR & Attendance'),
    ]

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    report_category = models.CharField(max_length=30, choices=REPORT_CATEGORIES)
    description = models.TextField(blank=True)
    parameters_schema = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_report_definitions'
        verbose_name = 'Report Definition'
        verbose_name_plural = 'Report Definitions'

    def __str__(self):
        return f"{self.name} ({self.code})"


class ReportExecution(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    report_definition = models.ForeignKey(ReportDefinition, on_delete=models.CASCADE, related_name='executions')
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='report_executions'
    )
    parameters = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    execution_duration_seconds = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    result_summary = models.JSONField(default=dict, blank=True)
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'df_report_executions'
        verbose_name = 'Report Execution'
        verbose_name_plural = 'Report Executions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.report_definition.name} run at {self.created_at.strftime('%Y-%m-%d %H:%M')} [{self.status}]"


class ReportSchedule(BaseModel):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily (End of Day)'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    report_definition = models.ForeignKey(ReportDefinition, on_delete=models.CASCADE, related_name='schedules')
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='report_schedules'
    )
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='DAILY')
    recipients_email_list = models.TextField(help_text="Comma-separated emails")
    next_run_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_report_schedules'
        verbose_name = 'Report Schedule'
        verbose_name_plural = 'Report Schedules'

    def __str__(self):
        return f"{self.report_definition.name} ({self.frequency})"


class ReportExport(BaseModel):
    FORMATS = [
        ('PDF', 'PDF Document'),
        ('EXCEL', 'Excel (.xlsx)'),
        ('CSV', 'CSV Document'),
        ('JSON', 'JSON Data'),
    ]

    execution = models.ForeignKey(ReportExecution, on_delete=models.CASCADE, related_name='exports')
    file_format = models.CharField(max_length=10, choices=FORMATS, default='PDF')
    file_path = models.CharField(max_length=255)
    file_size_bytes = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    generated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_report_exports'
        verbose_name = 'Report Export'
        verbose_name_plural = 'Report Exports'

    def __str__(self):
        return f"Export #{self.id} ({self.file_format}) - {self.file_size_bytes} bytes"
