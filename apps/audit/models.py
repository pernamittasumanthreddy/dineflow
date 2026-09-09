"""Enterprise Audit Trail, Diff Tracking, and Immutable Action Ledger Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class AuditAction(models.TextChoices):
    CREATE = 'CREATE', 'Created Entity'
    UPDATE = 'UPDATE', 'Updated Record'
    DELETE = 'DELETE', 'Deleted Entity'
    PRICE_CHANGE = 'PRICE_CHANGE', 'Menu Price Modified'
    ORDER_CANCEL = 'ORDER_CANCEL', 'Order Cancelled'
    REFUND_APPROVE = 'REFUND_APPROVE', 'Refund Approved'
    STOCK_ADJUST = 'STOCK_ADJUST', 'Inventory Stock Adjusted'
    PAYROLL_RUN = 'PAYROLL_RUN', 'Monthly Payroll Generated'

class AuditLog(TimeStampedModel):
    """Immutable system-wide ledger recording actor, change diff, timestamp, and IP."""
    actor = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=30, choices=AuditAction.choices, db_index=True)
    module_name = models.CharField('App / Module', max_length=50, db_index=True)
    object_id = models.CharField('Target ID', max_length=100, blank=True)
    object_repr = models.CharField('Object Summary', max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Audit Diffs
    old_values = models.JSONField('Previous State', default=dict, blank=True)
    new_values = models.JSONField('New State', default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']

    def __str__(self):
        actor_name = self.actor.display_name if self.actor else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {actor_name} performed {self.action} on {self.object_repr}"
