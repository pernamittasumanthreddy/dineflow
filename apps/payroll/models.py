"""Indian Payroll Engine, Statutory EPF/ESI/TDS Deductions, and Payslip Models."""
from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel

class PayrollStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    APPROVED = 'APPROVED', 'Approved by Manager'
    PAID = 'PAID', 'Disbursed / Paid'

class Payroll(TimeStampedModel):
    """Monthly payslip entity generated for an employee."""
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='payrolls')
    month = models.PositiveIntegerField('Month (1-12)')
    year = models.PositiveIntegerField('Year')
    status = models.CharField(max_length=20, choices=PayrollStatus.choices, default=PayrollStatus.DRAFT, db_index=True)
    
    # Days tracking
    total_days = models.PositiveIntegerField(default=30)
    days_worked = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('26.0'))
    loss_of_pay_days = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    
    # Earnings (₹ INR)
    basic_salary = models.DecimalField('Basic Salary (₹)', max_digits=10, decimal_places=2)
    hra_allowance = models.DecimalField('HRA (₹)', max_digits=10, decimal_places=2)
    conveyance_allowance = models.DecimalField('Conveyance (₹)', max_digits=10, decimal_places=2)
    special_allowance = models.DecimalField('Special Allowance (₹)', max_digits=10, decimal_places=2)
    overtime_pay = models.DecimalField('Overtime Pay (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    bonus_amount = models.DecimalField('Incentive / Bonus (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gross_earnings = models.DecimalField('Gross Earnings (₹)', max_digits=12, decimal_places=2)
    
    # Statutory & Attendance Deductions (₹ INR)
    lop_deduction = models.DecimalField('Loss of Pay Deduction (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    epf_deduction = models.DecimalField('EPF (Employee 12%) (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    esi_deduction = models.DecimalField('ESIC (0.75%) (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    professional_tax = models.DecimalField('Professional Tax (PT) (₹)', max_digits=10, decimal_places=2, default=Decimal('200.00'))
    tds_deduction = models.DecimalField('Income Tax / TDS (₹)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_deductions = models.DecimalField('Total Deductions (₹)', max_digits=12, decimal_places=2)
    
    # Net Pay
    net_salary = models.DecimalField('Net Disbursable Salary (₹)', max_digits=12, decimal_places=2)
    
    # Signatures
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='generated_payrolls')
    disbursed_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField('Bank NEFT/IMPS Ref', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Monthly Payslip'
        verbose_name_plural = 'Monthly Payslips'
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month', 'employee__employee_id']

    def __str__(self):
        return f"Payslip: {self.employee.employee_id} for {self.month}/{self.year} - Net ₹{self.net_salary}"

    def calculate_payroll(self):
        """Standard Indian payroll computation engine with LOP and EPF."""
        emp = self.employee
        per_day_rate = emp.gross_monthly_salary / Decimal(str(self.total_days or 30))
        
        # LOP deduction for unapproved absences
        self.lop_deduction = (per_day_rate * self.loss_of_pay_days).quantize(Decimal('0.01'))
        
        # Effective Earnings
        self.basic_salary = emp.basic_salary
        self.hra_allowance = emp.hra_allowance
        self.conveyance_allowance = emp.conveyance_allowance
        self.special_allowance = emp.special_allowance
        
        self.gross_earnings = (
            self.basic_salary + self.hra_allowance + self.conveyance_allowance +
            self.special_allowance + self.overtime_pay + self.bonus_amount
        ).quantize(Decimal('0.01'))
        
        # Deductions
        # EPF: 12% of basic (capped at ₹15,000 statutory limit = ₹1,800/mo or on actuals)
        capped_basic = min(self.basic_salary, Decimal('15000.00'))
        self.epf_deduction = (capped_basic * Decimal('0.12')).quantize(Decimal('0.01'))
        
        # ESIC: 0.75% of gross if gross <= ₹21,000
        if self.gross_earnings <= Decimal('21000.00'):
            self.esi_deduction = (self.gross_earnings * Decimal('0.0075')).quantize(Decimal('0.01'))
        else:
            self.esi_deduction = Decimal('0.00')
            
        self.professional_tax = Decimal('200.00')  # Standard state PT
        
        self.total_deductions = (
            self.lop_deduction + self.epf_deduction + self.esi_deduction +
            self.professional_tax + self.tds_deduction
        ).quantize(Decimal('0.01'))
        
        self.net_salary = max(Decimal('0.00'), (self.gross_earnings - self.total_deductions).quantize(Decimal('0.01')))
        self.save()
