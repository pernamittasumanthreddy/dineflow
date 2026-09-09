from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from apps.core.models import BaseModel, Branch, User


class KitchenStation(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='kitchen_stations')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    printer_ip = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_kitchen_stations'
        verbose_name = 'Kitchen Station'
        verbose_name_plural = 'Kitchen Stations'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'code'], name='unique_station_code_per_branch')
        ]

    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class KitchenOrder(BaseModel):
    STATUS_CHOICES = [
        ('RECEIVED', 'Received'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='kitchen_orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='kitchen_orders')
    station = models.ForeignKey(
        KitchenStation, on_delete=models.SET_NULL, null=True, blank=True, related_name='kitchen_orders'
    )
    kot_number = models.CharField(max_length=50, db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED', db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_kitchen_orders'
        verbose_name = 'Kitchen Order (KOT)'
        verbose_name_plural = 'Kitchen Orders (KOT)'
        indexes = [
            models.Index(fields=['branch', 'status', 'created_at']),
        ]

    def __str__(self):
        return f"KOT #{self.kot_number} - Order #{self.order.order_number} [{self.status}]"


class KitchenOrderItem(BaseModel):
    kitchen_order = models.ForeignKey(KitchenOrder, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, related_name='kitchen_items')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=KitchenOrder.STATUS_CHOICES, default='RECEIVED')
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_kitchen_order_items'
        verbose_name = 'Kitchen Order Item'
        verbose_name_plural = 'Kitchen Order Items'
        constraints = [
            CheckConstraint(condition=Q(quantity__gt=0), name='kot_item_qty_positive')
        ]

    def __str__(self):
        return f"{self.quantity}x {self.order_item.menu_item.name} (KOT #{self.kitchen_order.kot_number})"


class KitchenStatusHistory(BaseModel):
    kitchen_order = models.ForeignKey(KitchenOrder, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'df_kitchen_status_history'
        verbose_name = 'Kitchen Status History'
        verbose_name_plural = 'Kitchen Status Histories'
        ordering = ['-timestamp']

    def __str__(self):
        return f"KOT #{self.kitchen_order.kot_number}: {self.old_status} -> {self.new_status}"


class PreparationTimer(BaseModel):
    kitchen_order = models.ForeignKey(KitchenOrder, on_delete=models.CASCADE, related_name='timers')
    kitchen_order_item = models.ForeignKey(
        KitchenOrderItem, on_delete=models.CASCADE, null=True, blank=True, related_name='timers'
    )
    start_time = models.DateTimeField(null=True, blank=True)
    estimated_duration_minutes = models.PositiveIntegerField(default=15)
    target_ready_time = models.DateTimeField(null=True, blank=True)
    actual_ready_time = models.DateTimeField(null=True, blank=True)
    delay_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'df_preparation_timers'
        verbose_name = 'Preparation Timer'
        verbose_name_plural = 'Preparation Timers'

    def __str__(self):
        return f"Timer for KOT #{self.kitchen_order.kot_number} ({self.estimated_duration_minutes}m)"
