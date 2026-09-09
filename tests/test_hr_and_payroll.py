"""Comprehensive Test Suite for HR Staff Profiles, Attendance, Roster, and Indian Statutory Payroll."""
from decimal import Decimal
from datetime import time, date
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.employees.models import Department, Designation, Employee
from apps.shifts.models import Shift, ShiftRoster
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.payroll.models import Payroll, PayrollStatus

User = get_user_model()

class HRAndPayrollTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="hr@royalnizam.in",
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
            address="Road No 12, Banjara Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
            phone="+91 40 2334 1100"
        )
        self.hr_user = User.objects.create_user(
            email="hr@dineflow.in",
            username="hr_user",
            role=RoleChoices.HR,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.steward_user = User.objects.create_user(
            email="steward@dineflow.in",
            username="steward_arjun",
            role=RoleChoices.WAITER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.dept = Department.objects.create(
            name="Food & Beverage Service",
            description="Front of house guest dining service"
        )
        self.desig = Designation.objects.create(
            department=self.dept,
            title="Senior Captain"
        )
        self.employee = Employee.objects.create(
            user=self.steward_user,
            branch=self.branch,
            department=self.dept,
            designation=self.desig,
            employee_id="EMP-2026-002",
            date_of_joining=date(2025, 1, 15),
            basic_salary=Decimal('12000.00'),
            hra_allowance=Decimal('6000.00'),
            conveyance_allowance=Decimal('2000.00'),
            special_allowance=Decimal('4000.00'),
            pan_number="AAAPZ1234F",
            aadhaar_number="123456789012",
            uan_number="100987654321",
            bank_account_number="9100200123",
            ifsc_code="HDFC0001234"
        )

    def test_employee_gross_salary_calculation(self):
        """Test gross monthly salary aggregation (Basic + HRA + Conveyance + Special)."""
        # 12,000 + 6,000 + 2,000 + 4,000 = 24,000 INR
        self.assertEqual(self.employee.gross_monthly_salary, Decimal('24000.00'))

    def test_attendance_and_total_hours_property(self):
        """Test punch-in/out attendance tracking and total hours calculation."""
        record = AttendanceRecord.objects.create(
            employee=self.employee,
            date=timezone.localdate(),
            status=AttendanceStatus.PRESENT,
            check_in=time(10, 0),
            check_out=time(18, 30)
        )
        # 10:00 to 18:30 = 8.5 hours
        self.assertEqual(record.total_hours, 8.5)

    def test_shift_roster_assignment(self):
        """Test assigning employee to morning or dinner shift roster."""
        shift = Shift.objects.create(
            name="Dinner Service",
            start_time=time(17, 0),
            end_time=time(23, 30)
        )
        roster = ShiftRoster.objects.create(
            employee=self.employee,
            shift=shift,
            date=timezone.localdate(),
            status='SCHEDULED',
            notes="Counter Table 1-6"
        )
        self.assertEqual(roster.employee.employee_id, "EMP-2026-002")
        self.assertEqual(roster.shift.name, "Dinner Service")

    def test_statutory_indian_payroll_computation(self):
        """Test monthly payslip generation with Indian statutory EPF, ESIC, and PT deductions."""
        payroll = Payroll.objects.create(
            employee=self.employee,
            month=9,
            year=2026,
            status=PayrollStatus.DRAFT,
            total_days=30,
            days_worked=Decimal('26.0'),
            loss_of_pay_days=Decimal('0.0'),
            basic_salary=Decimal('12000.00'),
            hra_allowance=Decimal('6000.00'),
            conveyance_allowance=Decimal('2000.00'),
            special_allowance=Decimal('4000.00'),
            gross_earnings=Decimal('24000.00'),
            total_deductions=Decimal('0.00'),
            net_salary=Decimal('0.00'),
            generated_by=self.hr_user
        )
        # Execute statutory calculation engine
        payroll.calculate_payroll()

        # Gross = 24,000 INR
        self.assertEqual(payroll.gross_earnings, Decimal('24000.00'))
        
        # EPF: 12% of basic (12,000) = 1,440.00 INR
        self.assertEqual(payroll.epf_deduction, Decimal('1440.00'))

        # ESIC: Gross is 24,000 > 21,000 threshold -> 0.00
        self.assertEqual(payroll.esi_deduction, Decimal('0.00'))

        # Professional Tax: 200.00 INR standard
        self.assertEqual(payroll.professional_tax, Decimal('200.00'))

        # Total deductions = 1,440 (EPF) + 200 (PT) = 1,640.00 INR
        self.assertEqual(payroll.total_deductions, Decimal('1640.00'))

        # Net Salary = 24,000 - 1,640 = 22,360.00 INR
        self.assertEqual(payroll.net_salary, Decimal('22360.00'))
