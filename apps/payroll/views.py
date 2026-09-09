"""Indian Payroll Generation, Payslip Documents, and Salary Disbursal Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.payroll.models import Payroll, PayrollStatus
from apps.employees.models import Employee
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('payroll')
def payroll_list_view(request):
    """Payroll registry grouped by month and year with total outlay."""
    branch = request.user.branch
    today = timezone.localdate()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))

    payrolls = Payroll.objects.filter(month=selected_month, year=selected_year).select_related('employee__user', 'employee__designation')
    if branch:
        payrolls = payrolls.filter(employee__branch=branch)

    total_gross = sum(p.gross_earnings for p in payrolls)
    total_net = sum(p.net_salary for p in payrolls)
    total_epf = sum(p.epf_deduction for p in payrolls)

    months = [(i, timezone.datetime(2026, i, 1).strftime('%B')) for i in range(1, 13)]

    return render(request, 'payroll/payroll_list.html', {
        'payrolls': payrolls,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,
        'total_gross': total_gross,
        'total_net': total_net,
        'total_epf': total_epf,
    })

@login_required
@module_permission_required('payroll')
def payroll_generate_month_view(request):
    """Batch generates monthly payroll for all active branch employees."""
    today = timezone.localdate()
    month = int(request.POST.get('month', today.month))
    year = int(request.POST.get('year', today.year))
    branch = request.user.branch

    employees = Employee.objects.filter(is_active=True)
    if branch:
        employees = employees.filter(branch=branch)

    count = 0
    for emp in employees:
        # Calculate unexcused absences
        absent_days = AttendanceRecord.objects.filter(
            employee=emp,
            date__year=year,
            date__month=month,
            status=AttendanceStatus.ABSENT
        ).count()
        
        # Calculate overtime hours
        ot_records = AttendanceRecord.objects.filter(
            employee=emp,
            date__year=year,
            date__month=month
        )
        total_ot_hours = sum(r.overtime_hours for r in ot_records)
        hourly_rate = (emp.gross_monthly_salary / Decimal('200.00'))  # ~200 working hours/month
        ot_pay = (Decimal(str(total_ot_hours)) * hourly_rate * Decimal('1.5')).quantize(Decimal('0.01'))

        payroll, created = Payroll.objects.get_or_create(
            employee=emp,
            month=month,
            year=year,
            defaults={
                'basic_salary': emp.basic_salary,
                'hra_allowance': emp.hra_allowance,
                'conveyance_allowance': emp.conveyance_allowance,
                'special_allowance': emp.special_allowance,
                'gross_earnings': emp.gross_monthly_salary,
                'total_deductions': Decimal('0.00'),
                'net_salary': emp.gross_monthly_salary,
                'loss_of_pay_days': Decimal(str(absent_days)),
                'overtime_pay': ot_pay,
                'generated_by': request.user
            }
        )
        payroll.loss_of_pay_days = Decimal(str(absent_days))
        payroll.overtime_pay = ot_pay
        payroll.calculate_payroll()
        count += 1

    messages.success(request, f"Generated / updated payroll for {count} employees for {month}/{year}.")
    return redirect(f"/payroll/?month={month}&year={year}")

@login_required
def payslip_detail_view(request, payroll_id):
    """Detailed printable salary slip view in INR."""
    payroll = get_object_or_404(
        Payroll.objects.select_related('employee__user', 'employee__department', 'employee__designation', 'employee__branch'),
        id=payroll_id
    )
    return render(request, 'payroll/payslip.html', {'payroll': payroll})

@login_required
@module_permission_required('payroll')
def payroll_disburse_view(request, payroll_id):
    """Mark salary as disbursed with bank transfer reference."""
    payroll = get_object_or_404(Payroll, id=payroll_id)
    ref = request.POST.get('reference', f"NEFT-{timezone.now().strftime('%Y%m%d%H%M')}")
    
    payroll.status = PayrollStatus.PAID
    payroll.payment_reference = ref
    payroll.disbursed_at = timezone.now()
    payroll.save(update_fields=['status', 'payment_reference', 'disbursed_at'])

    messages.success(request, f"Salary for {payroll.employee.employee_id} marked as PAID (Ref: {ref}).")
    return redirect('payroll:payslip', payroll_id=payroll.id)
