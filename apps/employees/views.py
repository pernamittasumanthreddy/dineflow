"""Employee Directory, Onboarding, and Salary Master Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.employees.models import Employee, Department, Designation
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('hr')
def employee_list_view(request):
    """Staff directory with branch, department, and designation filters."""
    branch = request.user.branch
    employees = Employee.objects.filter(is_active=True).select_related('user', 'department', 'designation', 'branch')
    
    if branch:
        employees = employees.filter(branch=branch)
        
    dept_filter = request.GET.get('department')
    if dept_filter:
        employees = employees.filter(department_id=dept_filter)

    departments = Department.objects.all()
    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'departments': departments,
        'selected_dept': dept_filter,
    })

@login_required
@module_permission_required('hr')
def employee_detail_view(request, employee_id):
    """Comprehensive employee profile with statutory details and payslip history."""
    employee = get_object_or_404(
        Employee.objects.select_related('user', 'department', 'designation', 'branch'),
        id=employee_id
    )
    payrolls = employee.payrolls.all()[:6]
    attendance_records = employee.attendance_records.all()[:15]
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'payrolls': payrolls,
        'attendance_records': attendance_records,
    })
