from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel, Branch, User


class AuditLog(BaseModel):
    ACTION_CHOICES = [
        ('CREATE', 'Create Object'),
        ('UPDATE', 'Update Object'),
        ('DELETE', 'Delete / Soft Delete'),
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('PERMISSION_CHANGE', 'Permission Change'),
        ('PAYMENT', 'Payment Captured'),
        ('REFUND', 'Refund Processed'),
        ('INVENTORY_ADJUSTMENT', 'Inventory Adjustment'),
        ('PAYROLL_APPROVAL', 'Payroll Approval'),
    ]

    action = models.CharField(max_length=30, choices=ACTION_CHOICES, db_index=True)
    model_name = models.CharField(max_length=100, db_index=True)
    object_id = models.CharField(max_length=100, db_index=True)
    object_repr = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_actions'
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    changes = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'df_audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]

    def __str__(self):
        user_str = self.user.email if self.user else 'System'
        return f"[{self.action}] {self.model_name}:{self.object_id} by {user_str} at {self.timestamp}"


class SecurityEvent(BaseModel):
    EVENT_TYPES = [
        ('FAILED_LOGIN', 'Failed Login Attempt'),
        ('BRUTE_FORCE_BLOCKED', 'Brute Force IP Blocked'),
        ('UNAUTHORIZED_ACCESS', 'Unauthorized Resource Access'),
        ('PASSWORD_CHANGED', 'Password Changed'),
        ('SESSION_HIJACK_SUSPECT', 'Suspicious Session Change'),
    ]

    SEVERITY_LEVELS = [
        ('INFO', 'Informational'),
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_events'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='MEDIUM')
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'df_security_events'
        verbose_name = 'Security Event'
        verbose_name_plural = 'Security Events'
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.severity}] {self.event_type} from {self.ip_address} at {self.timestamp}"


class LoginHistory(BaseModel):
    STATUS_CHOICES = [
        ('SUCCESS', 'Successful Login'),
        ('FAILED', 'Failed Password'),
        ('LOCKED', 'Account Locked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_records')
    login_time = models.DateTimeField(default=timezone.now, db_index=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')

    class Meta:
        db_table = 'df_login_histories'
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.email} - {self.status} at {self.login_time}"
