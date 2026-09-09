"""Employee Master, Regulatory Compliance, and Salary Structure Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Department(TimeStampedModel):
    """Operational units (Kitchen, Dining Service, Bar, Housekeeping, Admin)."""
    name = models.CharField('Department Name', max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']

    def __str__(self):
        return self.name

class Designation(TimeStampedModel):
    """Job titles (Head Chef, Sous Chef, Floor Captain, Steward, Cashier, Steward)."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    title = models.CharField('Job Title', max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
        ordering = ['department', 'title']

    def __str__(self):
        return f"{self.title} ({self.department.name})"

class Employee(TimeStampedModel, SoftDeleteModel):
    """Comprehensive employee profile with Indian statutory identifiers and salary breakdown."""
    employee_id = models.CharField('Employee ID', max_length=30, unique=True, db_index=True)
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='employees'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees'
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees'
    )
    
    # Employment details
    date_of_joining = models.DateField('Joining Date')
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    
    # Statutory Indian identifiers
    pan_number = models.CharField('PAN Card #', max_length=10, blank=True)
    aadhaar_number = models.CharField('Aadhaar #', max_length=12, blank=True)
    uan_number = models.CharField('EPF UAN', max_length=12, blank=True)
    esi_number = models.CharField('ESIC Number', max_length=17, blank=True)
    
    # Banking details
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField('IFSC Code', max_length=20, blank=True)
    
    # Salary structure (in INR)
    basic_salary = models.DecimalField('Basic Salary (₹/month)', max_digits=10, decimal_places=2, default=Decimal('18000.00'))
    hra_allowance = models.DecimalField('HRA (₹/month)', max_digits=10, decimal_places=2, default=Decimal('7200.00'))
    conveyance_allowance = models.DecimalField('Conveyance (₹/month)', max_digits=10, decimal_places=2, default=Decimal('1600.00'))
    special_allowance = models.DecimalField('Special Allowance (₹/month)', max_digits=10, decimal_places=2, default=Decimal('3200.00'))
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username} ({self.designation.title if self.designation else 'Staff'})"

    @property
    def gross_monthly_salary(self):
        return self.basic_salary + self.hra_allowance + self.conveyance_allowance + self.special_allowance
