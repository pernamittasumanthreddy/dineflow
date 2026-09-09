import uuid

from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from apps.core.models import BaseModel, Branch


class TableSection(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='table_sections')
    name = models.CharField(max_length=100)
    floor = models.CharField(max_length=50, default='Ground Floor')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_table_sections'
        verbose_name = 'Table Section'
        verbose_name_plural = 'Table Sections'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'name'], name='unique_section_per_branch')
        ]

    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class RestaurantTable(BaseModel):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('RESERVED', 'Reserved'),
        ('BILLED', 'Billed'),
        ('CLEANING', 'Cleaning'),
        ('OUT_OF_SERVICE', 'Out of Service'),
    ]

    SHAPE_CHOICES = [
        ('SQUARE', 'Square'),
        ('ROUND', 'Round'),
        ('RECTANGLE', 'Rectangle'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='tables')
    section = models.ForeignKey(TableSection, on_delete=models.CASCADE, related_name='tables')
    table_number = models.CharField(max_length=20)
    seating_capacity = models.PositiveSmallIntegerField(default=4)
    min_capacity = models.PositiveSmallIntegerField(default=1)
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, default='RECTANGLE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', db_index=True)
    qr_code_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_restaurant_tables'
        verbose_name = 'Restaurant Table'
        verbose_name_plural = 'Restaurant Tables'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'table_number'], name='unique_table_per_branch'),
            CheckConstraint(condition=Q(seating_capacity__gt=0), name='table_seating_capacity_positive'),
            CheckConstraint(condition=Q(seating_capacity__gte=models.F('min_capacity')), name='capacity_gte_min_capacity'),
        ]
        indexes = [
            models.Index(fields=['branch', 'status']),
        ]

    def save(self, *args, **kwargs):
        if not self.qr_code_token:
            self.qr_code_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number} ({self.section.name} - {self.branch.name}) [{self.status}]"


class TableStatus(BaseModel):
    """
    Log of table occupancy transitions and turn-around analytics.
    """
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, related_name='status_logs')
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        'core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_status_changes'
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_table_status_logs'
        verbose_name = 'Table Status Log'
        verbose_name_plural = 'Table Status Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.table.table_number}: {self.previous_status} -> {self.new_status}"


class Reservation(BaseModel):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('CONFIRMED', 'Confirmed'),
        ('SEATED', 'Seated'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No-Show'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='reservations')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='reservations')
    reservation_number = models.CharField(max_length=50, unique=True, db_index=True)
    reservation_time = models.DateTimeField(db_index=True)
    party_size = models.PositiveSmallIntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED', db_index=True)
    special_requests = models.TextField(blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'df_reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        constraints = [
            CheckConstraint(condition=Q(party_size__gt=0), name='reservation_party_size_positive'),
            CheckConstraint(condition=Q(deposit_amount__gte=0), name='reservation_deposit_non_negative')
        ]
        indexes = [
            models.Index(fields=['branch', 'reservation_time', 'status']),
        ]

    def __str__(self):
        return f"Res #{self.reservation_number} - {self.customer.name} ({self.party_size} guests on {self.reservation_time.strftime('%Y-%m-%d %H:%M')})"


class ReservationGuest(BaseModel):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    guest_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_reservation_guests'
        verbose_name = 'Reservation Guest'
        verbose_name_plural = 'Reservation Guests'

    def __str__(self):
        return f"{self.guest_name} ({self.reservation.reservation_number})"


class TableAssignment(BaseModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, related_name='assignments')
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, null=True, blank=True, related_name='table_assignments'
    )
    waiter = models.ForeignKey(
        'employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_assignments'
    )
    assigned_at = models.DateTimeField(default=timezone.now)
    released_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        db_table = 'df_table_assignments'
        verbose_name = 'Table Assignment'
        verbose_name_plural = 'Table Assignments'
        indexes = [
            models.Index(fields=['table', 'status']),
            models.Index(fields=['waiter', 'status']),
        ]

    def __str__(self):
        return f"{self.table.table_number} assigned to {self.waiter or 'Unassigned'} [{self.status}]"
