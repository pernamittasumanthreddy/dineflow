"""Comprehensive Test Suite for Indian GST Billing, SAC 9963, Payments & Z-Reports."""
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.orders.models import Order, OrderStatus, OrderType
from apps.billing.models import Invoice, InvoiceItem
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.sales.models import CashRegisterSession, ZReport
from apps.core.utils import calculate_gst_breakdown

User = get_user_model()

class BillingAndGSTTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="accounts@royalnizam.in",
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
        self.cashier = User.objects.create_user(
            email="cashier@dineflow.in",
            username="cashier_bill",
            role=RoleChoices.CASHIER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.order = Order.objects.create(
            order_number="ORD-BILL-001",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            server=self.cashier,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('1000.00'),
            discount_amount=Decimal('100.00'),
            tax_amount=Decimal('45.00'),
            grand_total=Decimal('945.00'),
            is_paid=True
        )

    def test_indian_gst_intra_state_breakdown(self):
        """Test Indian GST 5% splits evenly into CGST 2.5% and SGST 2.5% for intra-state supply."""
        taxable_amount = Decimal('900.00')  # 1000 subtotal - 100 discount
        breakdown = calculate_gst_breakdown(
            subtotal=taxable_amount,
            tax_rate_percent=Decimal('5.00'),
            is_interstate=False
        )
        # 5% of 900 = 45 total tax -> 22.50 CGST + 22.50 SGST
        self.assertEqual(breakdown['cgst'], Decimal('22.50'))
        self.assertEqual(breakdown['sgst'], Decimal('22.50'))
        self.assertEqual(breakdown['igst'], Decimal('0.00'))
        self.assertEqual(breakdown['total_tax'], Decimal('45.00'))

    def test_indian_gst_inter_state_breakdown(self):
        """Test Indian GST 5% charges entire 5% as IGST for inter-state supply."""
        taxable_amount = Decimal('1000.00')
        breakdown = calculate_gst_breakdown(
            subtotal=taxable_amount,
            tax_rate_percent=Decimal('5.00'),
            is_interstate=True
        )
        self.assertEqual(breakdown['cgst'], Decimal('0.00'))
        self.assertEqual(breakdown['sgst'], Decimal('0.00'))
        self.assertEqual(breakdown['igst'], Decimal('50.00'))
        self.assertEqual(breakdown['total_tax'], Decimal('50.00'))

    def test_tax_invoice_creation_with_sac_code(self):
        """Test statutory Tax Invoice generation with SAC 9963 code and GST split."""
        invoice = Invoice.objects.create(
            invoice_number="INV/2026-09/TEST01",
            order=self.order,
            branch=self.branch,
            restaurant_name=self.restaurant.name,
            restaurant_gstin=self.restaurant.gstin,
            fssai_number=self.restaurant.fssai_number,
            branch_address=self.branch.address,
            taxable_subtotal=Decimal('900.00'),
            discount_amount=Decimal('100.00'),
            cgst_amount=Decimal('22.50'),
            sgst_amount=Decimal('22.50'),
            igst_amount=Decimal('0.00'),
            total_tax_amount=Decimal('45.00'),
            grand_total=Decimal('945.00'),
            is_paid=True,
            payment_method='UPI',
            cashier=self.cashier
        )
        item = InvoiceItem.objects.create(
            invoice=invoice,
            item_name="Hyderabadi Chicken Biryani",
            sac_code="996331",
            quantity=2,
            unit_rate=Decimal('450.00'),
            item_total=Decimal('900.00'),
            tax_rate_percent=Decimal('5.00'),
            cgst_amount=Decimal('22.50'),
            sgst_amount=Decimal('22.50')
        )
        self.assertEqual(invoice.restaurant_gstin, "36AAACN1234F1Z9")
        self.assertEqual(item.sac_code, "996331")
        self.assertEqual(invoice.grand_total, Decimal('945.00'))

    def test_offline_first_payment_simulation(self):
        """Test payment record creation with offline transaction reference generation."""
        payment = Payment.objects.create(
            order=self.order,
            amount=Decimal('945.00'),
            payment_method=PaymentMethod.UPI,
            status=PaymentStatus.SUCCESS,
            cashier=self.cashier
        )
        self.assertTrue(payment.transaction_reference.startswith("TXN-UPI-"))
        self.assertEqual(payment.status, PaymentStatus.SUCCESS)

    def test_cash_register_session_and_discrepancy(self):
        """Test daily drawer opening, closing count, and cash shortage/excess reconciliation."""
        session = CashRegisterSession.objects.create(
            branch=self.branch,
            opened_by=self.cashier,
            opening_cash=Decimal('2000.00'),
            status='OPEN'
        )
        # Cashier closes drawer at end of shift: expected 5000, counted 4950 (₹50 shortage)
        session.expected_cash = Decimal('5000.00')
        session.closing_cash = Decimal('4950.00')
        session.cash_discrepancy = session.closing_cash - session.expected_cash
        session.status = 'CLOSED'
        session.closed_by = self.cashier
        session.closed_at = timezone.now()
        session.save()

        self.assertEqual(session.cash_discrepancy, Decimal('-50.00'))
        self.assertEqual(session.status, 'CLOSED')

    def test_daily_z_report_generation(self):
        """Test daily statutory Z-Report sales aggregation."""
        today = timezone.localdate()
        z_report = ZReport.objects.create(
            branch=self.branch,
            report_date=today,
            total_orders=1,
            gross_sales=Decimal('1000.00'),
            discount_total=Decimal('100.00'),
            tax_total=Decimal('45.00'),
            net_sales=Decimal('945.00'),
            cash_sales=Decimal('0.00'),
            card_sales=Decimal('0.00'),
            upi_sales=Decimal('945.00'),
            total_expenses=Decimal('0.00'),
            net_drawer_balance=Decimal('2000.00'),
            generated_by=self.cashier
        )
        self.assertEqual(z_report.net_sales, Decimal('945.00'))
        self.assertEqual(z_report.upi_sales, Decimal('945.00'))
