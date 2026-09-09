from django.db import models
from django.db.models import Q, CheckConstraint
from apps.core.models import BaseModel, Restaurant, Branch, User


class Department(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='departments')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'df_departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'code'], name='unique_department_code_per_restaurant')
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Designation(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'df_designations'
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self):
        return f"{self.title} - {self.department.name}"


class Employee(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    EMPLOYMENT_TYPES = [
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('CONTRACT', 'Contract'),
        ('INTERN', 'Intern'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('RESIGNED', 'Resigned'),
        ('TERMINATED', 'Terminated'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='employees')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
    employee_code = models.CharField(max_length=50, db_index=True)
    date_of_joining = models.DateField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Compliance & Banking
    pan_number = models.CharField(max_length=10, blank=True)
    aadhaar_masked = models.CharField(max_length=12, blank=True, help_text="Masked Aadhaar: XXXXXXXX1234")
    bank_account_number = models.CharField(max_length=35, blank=True)
    bank_ifsc = models.CharField(max_length=15, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)

    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='FULL_TIME')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', db_index=True)

    class Meta:
        db_table = 'df_employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'employee_code'], name='unique_employee_code_per_restaurant')
        ]
        indexes = [
            models.Index(fields=['branch', 'status']),
            models.Index(fields=['department', 'status']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_code})"


class Shift(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration_minutes = models.PositiveSmallIntegerField(default=30)

    class Meta:
        db_table = 'df_shifts'
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"


class ShiftAssignment(BaseModel):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shift_assignments')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='assignments')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='shift_assignments')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')

    class Meta:
        db_table = 'df_shift_assignments'
        verbose_name = 'Shift Assignment'
        verbose_name_plural = 'Shift Assignments'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_shift_per_date')
        ]
        indexes = [
            models.Index(fields=['branch', 'date']),
        ]

    def __str__(self):
        return f"{self.employee.employee_code} | {self.shift.name} on {self.date}"


class Attendance(BaseModel):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('HALF_DAY', 'Half Day'),
        ('LATE', 'Late'),
        ('ON_LEAVE', 'On Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(db_index=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT', db_index=True)
    work_duration_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'df_attendances'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_attendance_per_date')
        ]
        indexes = [
            models.Index(fields=['branch', 'date', 'status']),
        ]

    def __str__(self):
        return f"{self.employee.employee_code} - {self.date} [{self.status}]"


class LeaveType(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='leave_types')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    annual_quota_days = models.PositiveSmallIntegerField(default=12)
    is_paid = models.BooleanField(default=True)
    is_carry_forward = models.BooleanField(default=False)

    class Meta:
        db_table = 'df_leave_types'
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Leave(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='applications')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves'
    )
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'df_leaves'
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'
        indexes = [
            models.Index(fields=['employee', 'status']),
        ]

    def __str__(self):
        return f"{self.employee.employee_code} | {self.leave_type.code} ({self.start_date} to {self.end_date})"


class SalaryStructure(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    basic_pay = models.DecimalField(max_digits=12, decimal_places=2)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    special_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    conveyance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    provident_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    esi = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    professional_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tds = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    effective_from = models.DateField()

    class Meta:
        db_table = 'df_salary_structures'
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'
        constraints = [
            CheckConstraint(condition=Q(basic_pay__gte=0), name='salary_basic_pay_non_negative'),
            CheckConstraint(condition=Q(hra__gte=0), name='salary_hra_non_negative'),
            CheckConstraint(condition=Q(special_allowance__gte=0), name='salary_special_allowance_non_negative'),
            CheckConstraint(condition=Q(conveyance__gte=0), name='salary_conveyance_non_negative'),
        ]

    @property
    def gross_salary(self):
        return self.basic_pay + self.hra + self.special_allowance + self.conveyance

    @property
    def total_deductions(self):
        return self.provident_fund + self.esi + self.professional_tax + self.tds

    @property
    def net_salary(self):
        return self.gross_salary - self.total_deductions

    def __str__(self):
        return f"Salary for {self.employee.employee_code} - Basic: {self.basic_pay}"


class Payroll(BaseModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PROCESSED', 'Processed'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='payrolls')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='payrolls')
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    total_gross = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_net = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT', db_index=True)
    approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payrolls'
    )
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'df_payrolls'
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'year', 'month'], name='unique_branch_monthly_payroll'),
            CheckConstraint(condition=Q(month__gte=1) & Q(month__lte=12), name='payroll_valid_month'),
            CheckConstraint(condition=Q(total_gross__gte=0), name='payroll_gross_non_negative'),
            CheckConstraint(condition=Q(total_net__gte=0), name='payroll_net_non_negative'),
        ]

    def __str__(self):
        return f"Payroll {self.branch.name} - {self.month:02d}/{self.year} [{self.status}]"


class PayrollItem(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('ON_HOLD', 'On Hold'),
    ]

    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='items')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='payroll_records')
    days_present = models.DecimalField(max_digits=4, decimal_places=1, default=30.0)
    basic_earned = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    pf_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    esi_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pt_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tds_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'df_payroll_items'
        verbose_name = 'Payroll Item'
        verbose_name_plural = 'Payroll Items'
        constraints = [
            CheckConstraint(condition=Q(gross_salary__gte=0), name='payroll_item_gross_non_negative'),
            CheckConstraint(condition=Q(net_salary__gte=0), name='payroll_item_net_non_negative'),
        ]

    def __str__(self):
        return f"{self.employee.employee_code} - Net: {self.net_salary}"
