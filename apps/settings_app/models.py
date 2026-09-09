from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel, Branch, Restaurant, User


class SystemSetting(BaseModel):
    SETTING_TYPES = [
        ('STRING', 'String'),
        ('INT', 'Integer'),
        ('FLOAT', 'Float'),
        ('BOOLEAN', 'Boolean'),
        ('JSON', 'JSON Object'),
    ]

    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    value_type = models.CharField(max_length=20, choices=SETTING_TYPES, default='STRING')
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_system_settings'
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'

    def __str__(self):
        return f"{self.key} = {self.value}"


class RestaurantSetting(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='custom_settings')
    key = models.CharField(max_length=100)
    value = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'df_restaurant_custom_settings'
        verbose_name = 'Restaurant Setting'
        verbose_name_plural = 'Restaurant Settings'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'key'], name='unique_restaurant_setting_key')
        ]

    def __str__(self):
        return f"{self.restaurant.name}: {self.key}"


class BranchSetting(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='custom_settings')
    key = models.CharField(max_length=100)
    value = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'df_branch_custom_settings'
        verbose_name = 'Branch Setting'
        verbose_name_plural = 'Branch Settings'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'key'], name='unique_branch_setting_key')
        ]

    def __str__(self):
        return f"{self.branch.name}: {self.key}"


class NotificationSetting(BaseModel):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='notification_settings'
    )
    email_host = models.CharField(max_length=150, blank=True)
    email_port = models.PositiveIntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_sender = models.EmailField(blank=True)
    sms_sender_id = models.CharField(max_length=20, blank=True, help_text="DLT registered header for India SMS")
    is_sms_active = models.BooleanField(default=False)
    is_whatsapp_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_notification_settings'
        verbose_name = 'Notification Setting'
        verbose_name_plural = 'Notification Settings'

    def __str__(self):
        branch_str = self.branch.name if self.branch else 'System Default'
        return f"Notification Setting ({branch_str})"


class BackupRecord(BaseModel):
    BACKUP_TYPES = [
        ('FULL_SQLITE', 'Full SQLite Backup'),
        ('POSTGRES_DUMP', 'PostgreSQL pg_dump'),
        ('SCHEMA_ONLY', 'Schema Only'),
        ('DATA_FIXTURES', 'Data Fixtures (JSON)'),
    ]

    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('RESTORED', 'Restored'),
    ]

    RESTORE_STATUS = [
        ('NOT_RESTORED', 'Not Restored'),
        ('RESTORE_VERIFIED', 'Restore Verified'),
        ('RESTORE_FAILED', 'Restore Failed'),
    ]

    backup_id = models.CharField(max_length=50, unique=True, db_index=True)
    backup_type = models.CharField(max_length=30, choices=BACKUP_TYPES, default='FULL_SQLITE')
    file_path = models.CharField(max_length=255)
    file_size_bytes = models.PositiveBigIntegerField(default=0)
    checksum_sha256 = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS', db_index=True)
    restore_status = models.CharField(max_length=30, choices=RESTORE_STATUS, default='NOT_RESTORED')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    restored_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_backup_records'
        verbose_name = 'Database Backup Record'
        verbose_name_plural = 'Database Backup Records'
        ordering = ['-created_at']

    def __str__(self):
        return f"Backup {self.backup_id} ({self.backup_type}) - {self.status} [{self.file_size_bytes} bytes]"
