"""Time-Clock, Punch-In/Out, and Overtime Tracking Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', 'Present'
    LATE = 'LATE', 'Late Arrival'
    HALF_DAY = 'HALF_DAY', 'Half Day'
    ABSENT = 'ABSENT', 'Absent (LOP)'
    ON_LEAVE = 'ON_LEAVE', 'Approved Leave'
    WEEKLY_OFF = 'WEEKLY_OFF', 'Weekly Off'

class AttendanceRecord(TimeStampedModel):
    """Daily check-in / check-out time log per staff member."""
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField('Attendance Date', db_index=True)
    check_in = models.TimeField('Check-in Time', null=True, blank=True)
    check_out = models.TimeField('Check-out Time', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
        db_index=True
    )
    
    # Deviations
    late_minutes = models.PositiveIntegerField('Late Arrival (Minutes)', default=0)
    early_departure_minutes = models.PositiveIntegerField('Early Departure (Minutes)', default=0)
    overtime_hours = models.DecimalField('Overtime (Hours)', max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    # Verification
    verified_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_attendance'
    )
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee__employee_id']

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} [{self.get_status_display()}]"

    @property
    def total_hours(self):
        if self.check_in and self.check_out:
            import datetime
            d = datetime.date(2026, 1, 1)
            t1 = datetime.datetime.combine(d, self.check_in)
            t2 = datetime.datetime.combine(d, self.check_out)
            return round((t2 - t1).total_seconds() / 3600.0, 1)
        elif self.check_in:
            return Decimal('4.0')
        return Decimal('0.0')
