"""Staff Shift Rostering, Schedules, and Break Tracking Models."""
from django.db import models
from apps.core.models import TimeStampedModel

class Shift(TimeStampedModel):
    """Standard operational shift template (Morning, Afternoon, Dinner, Night)."""
    name = models.CharField('Shift Name', max_length=100)
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')
    break_duration_minutes = models.PositiveIntegerField('Break Allowance (Mins)', default=45)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Shift Template'
        verbose_name_plural = 'Shift Templates'
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class ShiftRoster(TimeStampedModel):
    """Staff scheduling on designated shifts per date."""
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='scheduled_shifts')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='rosters')
    date = models.DateField('Roster Date', db_index=True)
    status = models.CharField(
        max_length=20,
        choices=[('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('SWAPPED', 'Swapped'), ('ABSENT', 'Absent')],
        default='SCHEDULED'
    )
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Shift Roster'
        verbose_name_plural = 'Shift Rosters'
        unique_together = ('employee', 'date')
        ordering = ['date', 'shift__start_time']

    def __str__(self):
        return f"{self.employee.employee_id} on {self.shift.name} ({self.date})"
