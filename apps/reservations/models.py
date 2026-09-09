"""Customer Dining Reservation and Table Booking Models."""
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel

class ReservationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Confirmation'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    SEATED = 'SEATED', 'Guest Seated'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    NO_SHOW = 'NO_SHOW', 'No-Show'

class Reservation(TimeStampedModel, SoftDeleteModel):
    """Guest table booking with party size, time slots, and status lifecycle."""
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )
    guest_name = models.CharField('Guest Name', max_length=120)
    guest_phone = models.CharField('Phone Number', max_length=20)
    guest_email = models.EmailField('Email Address', blank=True)
    
    # Booking details
    reservation_date = models.DateField('Booking Date')
    reservation_time = models.TimeField('Booking Time')
    guest_count = models.PositiveIntegerField('Guests Count', default=2)
    assigned_table = models.ForeignKey(
        'tables.RestaurantTable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )
    status = models.CharField(
        'Status',
        max_length=25,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
        db_index=True
    )
    special_requests = models.TextField('Special Requests / Dietary Preferences', blank=True)
    booked_by_staff = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booked_reservations'
    )

    class Meta:
        verbose_name = 'Table Reservation'
        verbose_name_plural = 'Table Reservations'
        ordering = ['reservation_date', 'reservation_time']

    def __str__(self):
        return f"Booking #{self.id}: {self.guest_name} ({self.guest_count} guests) on {self.reservation_date} {self.reservation_time}"
