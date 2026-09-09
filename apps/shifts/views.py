"""Staff Shift Scheduling and Rostering Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.shifts.models import Shift, ShiftRoster
from apps.employees.models import Employee
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('attendance')
def shift_roster_view(request):
    """Weekly staff roster view."""
    branch = request.user.branch
    today = timezone.localdate()
    selected_date = request.GET.get('date', str(today))
    
    rosters = ShiftRoster.objects.all().select_related('employee__user', 'shift')
    if branch:
        rosters = rosters.filter(employee__branch=branch)
    if selected_date:
        rosters = rosters.filter(date=selected_date)

    shifts = Shift.objects.all()
    employees = Employee.objects.filter(is_active=True)
    if branch:
        employees = employees.filter(branch=branch)

    return render(request, 'shifts/roster.html', {
        'rosters': rosters,
        'shifts': shifts,
        'employees': employees,
        'selected_date': selected_date,
    })
