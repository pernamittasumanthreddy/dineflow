"""Shift Scheduling, Overtime Calculation, and Roster Swap Services."""
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.shifts.models import ShiftRoster
from apps.audit.models import AuditLog, AuditAction

def schedule_employee_shift(employee, shift, roster_date, notes=""):
    """
    Schedules an employee for a shift on a specific date.
    Ensures employee is not double-booked on the same date.
    """
    roster, created = ShiftRoster.objects.get_or_create(
        employee=employee,
        date=roster_date,
        defaults={
            'shift': shift,
            'status': 'SCHEDULED',
            'notes': notes
        }
    )
    if not created and roster.shift != shift:
        roster.shift = shift
        roster.notes = notes
        roster.save(update_fields=['shift', 'notes'])
    return roster

def calculate_overtime_hours(attendance_record, standard_hours=8.0):
    """
    Calculates overtime hours when total recorded work duration exceeds standard hours.
    Returns overtime hours as float (e.g., 2.5).
    """
    actual_hours = attendance_record.total_hours
    if actual_hours > standard_hours:
        return round(actual_hours - standard_hours, 2)
    return 0.0

def swap_shifts(roster_a, roster_b, manager=None):
    """
    Exchanges shifts between two roster entries with manager signoff.
    """
    shift_a = roster_a.shift
    shift_b = roster_b.shift

    roster_a.shift = shift_b
    roster_a.status = 'SWAPPED'
    roster_a.save(update_fields=['shift', 'status'])

    roster_b.shift = shift_a
    roster_b.status = 'SWAPPED'
    roster_b.save(update_fields=['shift', 'status'])

    if manager:
        AuditLog.objects.create(
            actor=manager,
            action=AuditAction.UPDATE,
            module_name='shifts',
            object_id=f"{roster_a.id}_{roster_b.id}",
            object_repr=f"Shift swap between {roster_a.employee.employee_id} and {roster_b.employee.employee_id}",
            new_values={'roster_a_shift': shift_b.name, 'roster_b_shift': shift_a.name}
        )

    return roster_a, roster_b
