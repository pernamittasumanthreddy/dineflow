"""Time-Clock Terminal, Punch Clock-In/Out, and Monthly Attendance Log Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.employees.models import Employee
from apps.accounts.decorators import module_permission_required

@login_required
def time_clock_view(request):
    """
    Biometric / Digital Time-Clock punch terminal.
    Allows staff to punch in/out with automated late-arrival detection.
    """
    employee = getattr(request.user, 'employee_profile', None)
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    today_record = None
    if employee:
        today_record = AttendanceRecord.objects.filter(employee=employee, date=today).first()

    if request.method == 'POST':
        action = request.POST.get('action')
        emp_id = request.POST.get('employee_id')
        
        target_emp = employee
        if request.user.has_module_permission('attendance') and emp_id:
            target_emp = Employee.objects.filter(id=emp_id).first()
            
        if not target_emp:
            messages.error(request, "Employee profile not found.")
            return redirect('attendance:punch')

        record, created = AttendanceRecord.objects.get_or_create(
            employee=target_emp,
            date=today,
            defaults={'status': AttendanceStatus.PRESENT}
        )

        if action == 'PUNCH_IN':
            record.check_in = now_time
            # Late calculation (assuming 10:00 AM shift start)
            if now_time.hour > 10 or (now_time.hour == 10 and now_time.minute > 15):
                record.status = AttendanceStatus.LATE
                record.late_minutes = (now_time.hour - 10) * 60 + now_time.minute
            record.save()
            messages.success(request, f"Punch-In recorded for {target_emp.employee_id} at {now_time.strftime('%H:%M:%S')}")
        elif action == 'PUNCH_OUT':
            record.check_out = now_time
            if record.check_in:
                # Calculate hours
                hours = (datetime_combine(today, record.check_out) - datetime_combine(today, record.check_in)).total_seconds() / 3600.0
                if hours > 8.0:
                    record.overtime_hours = Decimal(str(round(hours - 8.0, 2)))
            record.save()
            messages.success(request, f"Punch-Out recorded for {target_emp.employee_id} at {now_time.strftime('%H:%M:%S')}")

        return redirect('attendance:punch')

    return render(request, 'attendance/punch_clock.html', {
        'employee': employee,
        'today_record': today_record,
        'today': today,
        'now_time': now_time,
    })

def datetime_combine(d, t):
    from datetime import datetime
    return datetime.combine(d, t)

@login_required
@module_permission_required('attendance')
def attendance_list_view(request):
    """Monthly attendance matrix and department logs."""
    branch = request.user.branch
    today = timezone.localdate()
    selected_date = request.GET.get('date', str(today))
    
    records = AttendanceRecord.objects.all().select_related('employee__user', 'employee__department')
    if branch:
        records = records.filter(employee__branch=branch)
    if selected_date:
        records = records.filter(date=selected_date)

    records = records.order_by('employee__employee_id')

    return render(request, 'attendance/attendance_list.html', {
        'records': records,
        'selected_date': selected_date,
        'statuses': AttendanceStatus.choices,
    })
