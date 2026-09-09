from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
    """
    Enterprise Roles for DineFlow ERP System.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    dashboard_url = models.CharField(max_length=200, default='/dashboard/owner/')
    icon = models.CharField(max_length=50, default='shield')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class UserProfile(models.Model):
    """
    Extended profile for authenticated ERP staff & guests.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    branch = models.CharField(max_length=150, default='Indiranagar Main (Bangalore)')
    employee_code = models.CharField(max_length=50, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    avatar_initials = models.CharField(max_length=5, default='DF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role.name}"

class Permission(models.Model):
    """
    Granular module capabilities.
    """
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    module = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.module} : {self.name} ({self.code})"

class RolePermission(models.Model):
    """
    Mapping between Roles and granular Permissions.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='roles')

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.code} -> {self.permission.code}"

class LoginHistory(models.Model):
    """
    Audit log of all authentication attempts.
    """
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED_CREDENTIALS', 'Invalid Credentials'),
        ('FAILED_ROLE_MISMATCH', 'Role Mismatch Rejection'),
        ('LOGOUT', 'Logged Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username_attempted = models.CharField(max_length=150)
    role_attempted = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username_attempted} [{self.role_attempted}] - {self.status} at {self.timestamp}"

class AuditLog(models.Model):
    """
    Immutable system activity audit trail.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.module}] {self.action} by {self.user} at {self.timestamp}"
