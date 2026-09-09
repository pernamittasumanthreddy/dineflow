"""Internal In-App Notifications and Broadcast Bus Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class NotificationType(models.TextChoices):
    LOW_STOCK = 'LOW_STOCK', 'Low Stock Alert'
    NEW_ORDER = 'NEW_ORDER', 'New Order Received'
    RESERVATION = 'RESERVATION', 'Guest Table Reservation'
    PAYMENT = 'PAYMENT', 'Payment Settlement'
    REFUND = 'REFUND', 'Refund Request / Approval'
    LEAVE = 'LEAVE', 'Staff Leave / Attendance'
    PAYROLL = 'PAYROLL', 'Monthly Payroll Disbursal'
    SYSTEM = 'SYSTEM', 'System Alert'

class Notification(TimeStampedModel):
    """In-app alert notification dispatched to users."""
    recipient = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Leave empty for all branch managers and admins'
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM,
        db_index=True
    )
    url = models.CharField('Redirect URL', max_length=255, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = 'Internal Notification'
        verbose_name_plural = 'Internal Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type}] {self.title} ({'Read' if self.is_read else 'Unread'})"
