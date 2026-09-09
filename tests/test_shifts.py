"""Comprehensive Test Suite for Shift Rostering, Overtime Detection, and Swap Services."""
from decimal import Decimal
from datetime import time, date
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.employees.models import Department, Designation, Employee
from apps.shifts.models import Shift, ShiftRoster
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.shifts.services import schedule_employee_shift, calculate_overtime_hours, swap_shifts
from apps.audit.models import AuditLog

User = get_user_model()

class ShiftsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="shifts@royalnizam.in",
            phone="+91 40 2334 5678",
            address_line1="Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500033"
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name="Banjara Hills Flagship",
            code="HYD-BANJARA",
            address="Road No 12",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
            phone="+91 40 2334 1100"
        )
        self.manager = User.objects.create_user(
            email="manager.shift@dineflow.in",
            username="mgr_shift",
            role=RoleChoices.MANAGER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.u1 = User.objects.create_user(
            email="staff1@dineflow.in", username="staff1", role=RoleChoices.WAITER, branch=self.branch, restaurant=self.restaurant
        )
        self.u2 = User.objects.create_user(
            email="staff2@dineflow.in", username="staff2", role=RoleChoices.WAITER, branch=self.branch, restaurant=self.restaurant
        )
        dept = Department.objects.create(name="F&B Service")
        desig = Designation.objects.create(department=dept, title="Captain")
        
        self.emp1 = Employee.objects.create(
            user=self.u1, branch=self.branch, department=dept, designation=desig, employee_id="EMP-SH-01",
            date_of_joining=date(2025, 1, 1), basic_salary=Decimal('10000.00'), hra_allowance=Decimal('5000.00'),
            conveyance_allowance=Decimal('2000.00'), special_allowance=Decimal('3000.00'),
            pan_number="AAAPZ1234F", aadhaar_number="123456789012", uan_number="100987654321"
        )
        self.emp2 = Employee.objects.create(
            user=self.u2, branch=self.branch, department=dept, designation=desig, employee_id="EMP-SH-02",
            date_of_joining=date(2025, 1, 1), basic_salary=Decimal('10000.00'), hra_allowance=Decimal('5000.00'),
            conveyance_allowance=Decimal('2000.00'), special_allowance=Decimal('3000.00'),
            pan_number="BBBPZ1234F", aadhaar_number="223456789012", uan_number="200987654321"
        )
        self.shift_morning = Shift.objects.create(
            name="Morning Service", start_time=time(10, 0), end_time=time(16, 0)
        )
        self.shift_dinner = Shift.objects.create(
            name="Dinner Service", start_time=time(17, 0), end_time=time(23, 0)
        )

    def test_schedule_employee_shift(self):
        """Test scheduling an employee on a shift date."""
        target_d = date(2026, 9, 15)
        roster = schedule_employee_shift(self.emp1, self.shift_morning, target_d, notes="Section A")
        self.assertEqual(roster.employee, self.emp1)
        self.assertEqual(roster.shift, self.shift_morning)
        self.assertEqual(roster.status, 'SCHEDULED')

    def test_calculate_overtime_hours(self):
        """Test overtime detection when total hours exceed 8.0 hours standard."""
        # 10.5 hours worked (10:00 to 20:30)
        att = AttendanceRecord.objects.create(
            employee=self.emp1,
            date=date(2026, 9, 15),
            status=AttendanceStatus.PRESENT,
            check_in=time(10, 0),
            check_out=time(20, 30)
        )
        ot = calculate_overtime_hours(att, standard_hours=8.0)
        # 10.5 - 8.0 = 2.5 hours overtime
        self.assertEqual(ot, 2.5)

    def test_swap_shifts(self):
        """Test swapping shifts between two employees with audit trail recording."""
        target_d = date(2026, 9, 15)
        r1 = ShiftRoster.objects.create(employee=self.emp1, shift=self.shift_morning, date=target_d, status='SCHEDULED')
        r2 = ShiftRoster.objects.create(employee=self.emp2, shift=self.shift_dinner, date=target_d, status='SCHEDULED')

        swap_shifts(r1, r2, manager=self.manager)

        r1.refresh_from_db()
        r2.refresh_from_db()

        # r1 now has Dinner Service, r2 has Morning Service
        self.assertEqual(r1.shift, self.shift_dinner)
        self.assertEqual(r2.shift, self.shift_morning)
        self.assertEqual(r1.status, 'SWAPPED')
        self.assertEqual(r2.status, 'SWAPPED')

        # Audit trail created
        log = AuditLog.objects.filter(module_name='shifts').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.actor, self.manager)
