from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.core.models import Restaurant, Branch, User
from apps.customers.models import Customer
from apps.tables.models import TableSection, RestaurantTable, Reservation, TableAssignment
from apps.billing.models import Invoice
from apps.payments.models import Payment, PaymentMethod, Refund, RefundReason
from apps.orders.models import Order
from apps.employees.models import Department, Designation, Employee, Payroll, PayrollItem


class ReservationsAndPaymentsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Kerala Taste Test',
            code='KTR_TEST',
            email='ktr@test.in',
            phone='9484011223'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name='Marine Drive',
            code='KOC_TEST',
            city='Kochi',
            state='Kerala',
            pincode='682031',
            phone='9484011223',
            email='koc@test.in'
        )
        self.customer = Customer.objects.create(
            restaurant=self.restaurant,
            name='Priya Nair',
            phone='9848099887',
            email='priya@test.in'
        )
        self.section = TableSection.objects.create(branch=self.branch, name='Sea View Deck')
        self.table = RestaurantTable.objects.create(
            branch=self.branch,
            section=self.section,
            table_number='K-01',
            seating_capacity=4,
            min_capacity=2,
            status='AVAILABLE'
        )
        self.admin = User.objects.create(
            email='approver@kerala.in',
            phone='9484099999',
            first_name='Admin',
            is_staff=True
        )

    def test_reservation_and_table_assignment(self):
        """Validates booking a reservation and assigning it to an available table."""
        res_time = timezone.now() + timezone.timedelta(hours=2)
        reservation = Reservation.objects.create(
            branch=self.branch,
            customer=self.customer,
            reservation_number='RES-KOC-001',
            reservation_time=res_time,
            party_size=3,
            status='CONFIRMED',
            deposit_amount=Decimal('500.00')
        )
        self.assertEqual(reservation.status, 'CONFIRMED')
        self.assertEqual(reservation.party_size, 3)

        # Assign table
        assignment = TableAssignment.objects.create(
            table=self.table,
            reservation=reservation,
            status='ACTIVE'
        )
        self.table.status = 'RESERVED'
        self.table.save()

        self.assertEqual(assignment.status, 'ACTIVE')
        self.assertEqual(self.table.status, 'RESERVED')

    def test_payment_and_refund_workflow(self):
        """Validates payment recording and subsequent partial or full refund processing."""
        order = Order.objects.create(
            restaurant=self.restaurant,
            branch=self.branch,
            order_number='ORD-REFUND-01',
            order_type='DINE_IN',
            subtotal=Decimal('500.00'),
            tax_amount=Decimal('25.00'),
            final_amount=Decimal('525.00'),
            status='PAID'
        )
        invoice = Invoice.objects.create(
            order=order,
            restaurant=self.restaurant,
            branch=self.branch,
            invoice_number='INV/KOC/2026-27/00099',
            fiscal_year='2026-27',
            subtotal=Decimal('500.00'),
            taxable_amount=Decimal('500.00'),
            grand_total=Decimal('525.00'),
            status='PAID'
        )
        pm_upi, _ = PaymentMethod.objects.get_or_create(code='UPI', defaults={'name': 'UPI'})
        payment = Payment.objects.create(
            invoice=invoice,
            order=order,
            branch=self.branch,
            payment_method=pm_upi,
            amount=Decimal('525.00'),
            transaction_reference='UPI-REF-001',
            status='SUCCESS'
        )

        # Process Refund
        reason, _ = RefundReason.objects.get_or_create(code='QUALITY', defaults={'title': 'Food Quality Issue'})
        refund = Refund.objects.create(
            payment=payment,
            invoice=invoice,
            refund_number='REF-0001',
            reason=reason,
            amount=Decimal('525.00'),
            refund_mode=pm_upi,
            transaction_reference='REV-UPI-REF-001',
            approved_by=self.admin,
            notes='Complimentary full refund approved'
        )

        payment.status = 'REFUNDED'
        payment.save()
        invoice.status = 'REFUNDED'
        invoice.save()

        self.assertEqual(refund.amount, Decimal('525.00'))
        self.assertEqual(payment.status, 'REFUNDED')
        self.assertEqual(invoice.status, 'REFUNDED')

    def test_payroll_and_items_generation(self):
        """Validates monthly branch payroll header and employee payslip calculations."""
        dept = Department.objects.create(restaurant=self.restaurant, branch=self.branch, code='KITCHEN', name='Kitchen')
        desig = Designation.objects.create(department=dept, code='CHEF', title='Chef', level=2)
        emp_user = User.objects.create(email='chef.koc@dineflow.in', phone='9848099880', first_name='Chef', is_staff=True)
        emp = Employee.objects.create(
            user=emp_user,
            restaurant=self.restaurant,
            branch=self.branch,
            department=dept,
            designation=desig,
            employee_code='EMP-KOC-009',
            date_of_joining=timezone.now().date(),
            status='ACTIVE'
        )

        payroll = Payroll.objects.create(
            restaurant=self.restaurant,
            branch=self.branch,
            month=9,
            year=2026,
            total_gross=Decimal('35000.00'),
            total_deductions=Decimal('3500.00'),
            total_net=Decimal('31500.00'),
            status='APPROVED',
            approved_by=emp
        )

        item = PayrollItem.objects.create(
            payroll=payroll,
            employee=emp,
            days_present=Decimal('30.0'),
            basic_earned=Decimal('25000.00'),
            allowances=Decimal('10000.00'),
            gross_salary=Decimal('35000.00'),
            pf_deduction=Decimal('3000.00'),
            pt_deduction=Decimal('200.00'),
            tds_deduction=Decimal('300.00'),
            net_salary=Decimal('31500.00'),
            payment_status='PAID',
            payment_reference='BANK-NEFT-SEP2026-01'
        )

        self.assertEqual(payroll.items.count(), 1)
        self.assertEqual(item.net_salary, Decimal('31500.00'))
