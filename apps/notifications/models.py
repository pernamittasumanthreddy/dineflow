from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel, Restaurant, Branch, User


class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('ORDER', 'New Order / Update'),
        ('KITCHEN', 'KOT Delay / Priority Alert'),
        ('LOW_STOCK', 'Low Stock Warning'),
        ('RESERVATION', 'Table Reservation Alert'),
        ('PAYROLL', 'Payroll Generated'),
        ('EXPENSE', 'Expense Pending Approval'),
        ('SYSTEM', 'System Security / Maintenance'),
    ]

    PRIORITIES = [
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    CHANNELS = [
        ('IN_APP', 'In-App'),
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications',
        help_text="Target user, or null if broadcast to branch/restaurant"
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='notifications')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='NORMAL')
    channel = models.CharField(max_length=20, choices=CHANNELS, default='IN_APP')
    action_url = models.CharField(max_length=255, blank=True)
    is_broadcast = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['restaurant', 'notification_type']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.notification_type}] {self.title}"


class NotificationPreference(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    order_alerts = models.BooleanField(default=True)
    stock_alerts = models.BooleanField(default=True)
    reservation_alerts = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"Preferences for {self.user.email}"


class NotificationReadStatus(BaseModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_reads')
    is_read = models.BooleanField(default=True)
    read_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_notification_read_statuses'
        verbose_name = 'Notification Read Status'
        verbose_name_plural = 'Notification Read Statuses'
        constraints = [
            models.UniqueConstraint(fields=['notification', 'user'], name='unique_notification_user_read')
        ]

    def __str__(self):
        return f"{self.user.email} read #{self.notification.id} at {self.read_at}"
