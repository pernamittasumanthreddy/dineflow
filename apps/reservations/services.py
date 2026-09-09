"""Table Reservation Booking, Time-Slot Conflict Detection & Seating Services."""
from datetime import datetime, timedelta, time
from django.core.exceptions import ValidationError
from apps.reservations.models import Reservation, ReservationStatus
from apps.tables.models import RestaurantTable, TableStatus
from apps.notifications.models import Notification, NotificationType

def check_table_conflict(table, booking_date, booking_time, buffer_minutes=90):
    """
    Checks if a table has an existing active reservation within +/- buffer_minutes.
    """
    dt_target = datetime.combine(booking_date, booking_time)
    
    existing_bookings = Reservation.objects.filter(
        assigned_table=table,
        reservation_date=booking_date,
        status__in=[ReservationStatus.PENDING, ReservationStatus.CONFIRMED, ReservationStatus.SEATED]
    )
    for b in existing_bookings:
        b_dt = datetime.combine(b.reservation_date, b.reservation_time)
        diff_mins = abs((dt_target - b_dt).total_seconds()) / 60.0
        if diff_mins < buffer_minutes:
            return True, b
    return False, None

def book_guest_reservation(branch, guest_name, guest_phone, booking_date, booking_time, guest_count, assigned_table=None, customer=None):
    """
    Creates a reservation. Validates party size against table capacity and detects time conflicts.
    """
    if assigned_table:
        if assigned_table.seating_capacity < guest_count:
            raise ValidationError(f"Table {assigned_table.table_number} capacity ({assigned_table.seating_capacity}) cannot seat {guest_count} guests.")
        
        has_conflict, conflicting_b = check_table_conflict(assigned_table, booking_date, booking_time)
        if has_conflict:
            raise ValidationError(f"Table {assigned_table.table_number} already has a reservation at {conflicting_b.reservation_time.strftime('%H:%M')} on {booking_date}.")

    reservation = Reservation.objects.create(
        branch=branch,
        customer=customer,
        guest_name=guest_name,
        guest_phone=guest_phone,
        reservation_date=booking_date,
        reservation_time=booking_time,
        guest_count=guest_count,
        assigned_table=assigned_table,
        status=ReservationStatus.CONFIRMED if assigned_table else ReservationStatus.PENDING
    )

    # Trigger internal notification
    Notification.objects.create(
        title=f"New Reservation: {guest_name} ({guest_count} guests)",
        message=f"Reservation booked for {booking_date} at {booking_time.strftime('%H:%M')}.",
        notification_type=NotificationType.RESERVATION,
        url="/reservations/"
    )

    return reservation

def seat_reservation(reservation):
    """
    Marks the reservation as SEATED and transitions table status to OCCUPIED.
    """
    reservation.status = ReservationStatus.SEATED
    reservation.save(update_fields=['status'])

    if reservation.assigned_table:
        reservation.assigned_table.status = TableStatus.OCCUPIED
        reservation.assigned_table.save(update_fields=['status'])

    return reservation

def cancel_or_no_show_reservation(reservation, is_no_show=False):
    """
    Cancels reservation or marks as NO_SHOW, freeing up the table.
    """
    reservation.status = ReservationStatus.NO_SHOW if is_no_show else ReservationStatus.CANCELLED
    reservation.save(update_fields=['status'])

    if reservation.assigned_table and reservation.assigned_table.status != TableStatus.OCCUPIED:
        reservation.assigned_table.status = TableStatus.AVAILABLE
        reservation.assigned_table.save(update_fields=['status'])

    return reservation
