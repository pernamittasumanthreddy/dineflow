from django.db import models
from django.utils import timezone
from apps.core.models import BaseModel, Branch, User


class DeliveryOrder(BaseModel):
    STATUS_CHOICES = [
        ('PENDING_ASSIGNMENT', 'Pending Rider Assignment'),
        ('ASSIGNED', 'Rider Assigned'),
        ('PICKED_UP', 'Picked Up / Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Delivery Failed'),
        ('RETURNED', 'Returned to Restaurant'),
    ]

    CHANNELS = [
        ('DIRECT', 'Direct Restaurant Delivery'),
        ('SWIGGY', 'Swiggy'),
        ('ZOMATO', 'Zomato'),
        ('DUNZO', 'Dunzo'),
    ]

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery_details')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='delivery_orders')
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='deliveries')
    delivery_channel = models.CharField(max_length=30, choices=CHANNELS, default='DIRECT')
    third_party_order_id = models.CharField(max_length=100, blank=True)
    estimated_delivery_time_minutes = models.PositiveIntegerField(default=45)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_ASSIGNMENT', db_index=True)

    class Meta:
        db_table = 'df_delivery_orders'
        verbose_name = 'Delivery Order'
        verbose_name_plural = 'Delivery Orders'
        indexes = [
            models.Index(fields=['branch', 'status']),
        ]

    def __str__(self):
        return f"Delivery for Order #{self.order.order_number} [{self.status}]"


class DeliveryAddress(BaseModel):
    delivery_order = models.OneToOneField(DeliveryOrder, on_delete=models.CASCADE, related_name='address')
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    delivery_instructions = models.TextField(blank=True)

    class Meta:
        db_table = 'df_delivery_addresses'
        verbose_name = 'Delivery Address'
        verbose_name_plural = 'Delivery Addresses'

    def __str__(self):
        return f"{self.contact_name} - {self.address_line1}, {self.city}"


class DeliveryAssignment(BaseModel):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    delivery_order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='assignments')
    rider = models.ForeignKey('employees.Employee', on_delete=models.PROTECT, related_name='delivery_assignments')
    assigned_at = models.DateTimeField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')

    class Meta:
        db_table = 'df_delivery_assignments'
        verbose_name = 'Delivery Assignment'
        verbose_name_plural = 'Delivery Assignments'

    def __str__(self):
        return f"Order #{self.delivery_order.order.order_number} -> Rider {self.rider.employee_code} [{self.status}]"


class DeliveryStatusHistory(BaseModel):
    delivery_order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_delivery_status_histories'
        verbose_name = 'Delivery Status History'
        verbose_name_plural = 'Delivery Status Histories'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Delivery #{self.delivery_order.id}: {self.old_status} -> {self.new_status}"
