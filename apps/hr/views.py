from django.shortcuts import render

def employee_list(request):
    """
    Staff Directory & Employee Master.
    """
    employees = [
        {'emp_id': 'EMP-101', 'name': 'Chef Sanjeev Teja', 'designation': 'Executive Chef', 'dept': 'Kitchen / Tandoor', 'mobile': '+91 98480 11223', 'branch': 'Indiranagar Main', 'doj': '12/04/2021', 'salary': 65000.00, 'status': 'active'},
        {'emp_id': 'EMP-102', 'name': 'Ravi Teja', 'designation': 'Head Captain (Waiter)', 'dept': 'Front of House', 'mobile': '+91 97000 44556', 'branch': 'Indiranagar Main', 'doj': '15/08/2022', 'salary': 28000.00, 'status': 'active'},
        {'emp_id': 'EMP-103', 'name': 'Sneha Reddy', 'designation': 'Cashier & POS Lead', 'dept': 'Finance / POS', 'mobile': '+91 98850 77889', 'branch': 'Indiranagar Main', 'doj': '01/02/2023', 'salary': 26000.00, 'status': 'active'},
        {'emp_id': 'EMP-104', 'name': 'Arjun Varma', 'designation': 'Captain (Service)', 'dept': 'Front of House', 'mobile': '+91 96180 22334', 'branch': 'Indiranagar Main', 'doj': '10/06/2023', 'salary': 24000.00, 'status': 'active'},
        {'emp_id': 'EMP-105', 'name': 'Naresh Babu', 'designation': 'Master Biryani Chef', 'dept': 'Kitchen / Biryani', 'mobile': '+91 94400 66778', 'branch': 'Indiranagar Main', 'doj': '18/11/2021', 'salary': 45000.00, 'status': 'active'},
    ]
    context = {
        'page_title': 'Employee Directory & Staff Master',
        'employees': employees
    }
    return render(request, 'hr/employee_list.html', context)

def attendance(request):
    """
    Biometric Attendance & Punch Log.
    """
    attendance_records = [
        {'emp_id': 'EMP-101', 'name': 'Chef Sanjeev Teja', 'date': '09/09/2026', 'shift': 'Split Shift', 'in_time': '10:45 AM', 'out_time': 'In Progress', 'hours': '3.8 hrs', 'status': 'present'},
        {'emp_id': 'EMP-102', 'name': 'Ravi Teja', 'date': '09/09/2026', 'shift': 'Morning Shift', 'in_time': '09:52 AM', 'out_time': 'In Progress', 'hours': '4.7 hrs', 'status': 'present'},
        {'emp_id': 'EMP-103', 'name': 'Sneha Reddy', 'date': '09/09/2026', 'shift': 'Evening Shift', 'in_time': '-', 'out_time': '-', 'hours': '-', 'status': 'pending'},
        {'emp_id': 'EMP-104', 'name': 'Arjun Varma', 'date': '09/09/2026', 'shift': 'Morning Shift', 'in_time': '10:14 AM', 'out_time': 'In Progress', 'hours': '4.3 hrs', 'status': 'late'},
    ]
    context = {
        'page_title': 'Biometric Attendance Logs',
        'records': attendance_records
    }
    return render(request, 'hr/attendance.html', context)

def shifts(request):
    """
    Shift Rosters & Scheduling.
    """
    shift_schedules = [
        {'shift_name': 'Morning Dining Shift', 'timing': '10:00 AM - 06:00 PM', 'staff_assigned': 14, 'supervisor': 'Ravi Teja', 'branch': 'Indiranagar Main'},
        {'shift_name': 'Evening Dinner Shift', 'timing': '04:00 PM - 12:00 Midnight', 'staff_assigned': 18, 'supervisor': 'Pavan Varma', 'branch': 'Indiranagar Main'},
        {'shift_name': 'Kitchen Split Shift', 'timing': '11:00 AM - 03:30 PM & 06:30 PM - 11:30 PM', 'staff_assigned': 8, 'supervisor': 'Chef Sanjeev Teja', 'branch': 'Indiranagar Main'},
    ]
    context = {
        'page_title': 'Shift Rosters & Scheduling',
        'shifts': shift_schedules
    }
    return render(request, 'hr/shifts.html', context)

def payroll(request):
    """
    Indian Payroll Processing (Basic, HRA, PF 12%, ESIC 0.75%, PT, TDS) & Payslips.
    """
    payroll_runs = [
        {'emp_id': 'EMP-101', 'name': 'Chef Sanjeev Teja', 'basic': 32500.00, 'hra': 16250.00, 'special': 16250.00, 'gross': 65000.00, 'pf': 3900.00, 'esic': 0.00, 'pt': 200.00, 'tds': 2400.00, 'net_salary': 58500.00, 'status': 'processed'},
        {'emp_id': 'EMP-102', 'name': 'Ravi Teja', 'basic': 14000.00, 'hra': 7000.00, 'special': 7000.00, 'gross': 28000.00, 'pf': 1680.00, 'esic': 210.00, 'pt': 200.00, 'tds': 0.00, 'net_salary': 25910.00, 'status': 'processed'},
        {'emp_id': 'EMP-103', 'name': 'Sneha Reddy', 'basic': 13000.00, 'hra': 6500.00, 'special': 6500.00, 'gross': 26000.00, 'pf': 1560.00, 'esic': 195.00, 'pt': 200.00, 'tds': 0.00, 'net_salary': 24045.00, 'status': 'processed'},
        {'emp_id': 'EMP-104', 'name': 'Arjun Varma', 'basic': 12000.00, 'hra': 6000.00, 'special': 6000.00, 'gross': 24000.00, 'pf': 1440.00, 'esic': 180.00, 'pt': 200.00, 'tds': 0.00, 'net_salary': 22180.00, 'status': 'processed'},
    ]
    context = {
        'page_title': 'Indian Payroll & Salary Slips',
        'payroll_runs': payroll_runs,
        'month': 'August 2026'
    }
    return render(request, 'hr/payroll.html', context)
