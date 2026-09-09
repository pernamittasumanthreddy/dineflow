"""Home Delivery Logistics, Rider Dispatch, and ETA Tracking Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class DeliveryStatus(models.TextChoices):
    PENDING_RIDER = 'PENDING_RIDER', 'Pending Rider Assignment'
    ASSIGNED = 'ASSIGNED', 'Rider Assigned'
    PICKED_UP = 'PICKED_UP', 'Picked Up from Kitchen'
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Out for Delivery'
    DELIVERED = 'DELIVERED', 'Delivered to Customer'
    FAILED = 'FAILED', 'Delivery Failed / Returned'

class DeliveryOrder(TimeStampedModel):
    """Delivery dispatch record linked to takeaway/delivery order."""
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery_dispatch')
    assigned_rider = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_deliveries'
    )
    recipient_name = models.CharField(max_length=150)
    recipient_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=25,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING_RIDER,
        db_index=True
    )
    
    # Timing
    estimated_delivery_minutes = models.PositiveIntegerField(default=35)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Delivery Dispatch'
        verbose_name_plural = 'Delivery Dispatches'
        ordering = ['-created_at']

    def __str__(self):
        return f"Delivery for Order #{self.order.order_number} to {self.recipient_name} [{self.status}]"
