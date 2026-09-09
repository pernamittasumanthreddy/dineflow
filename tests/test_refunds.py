"""Comprehensive Test Suite for Refund Workflow, Validations, and Manager Approvals."""
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.orders.models import Order, OrderStatus, OrderType
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.refunds.models import RefundRequest, RefundStatus
from apps.refunds.services import create_refund_request, approve_refund, reject_refund
from apps.audit.models import AuditLog, AuditAction

User = get_user_model()

class RefundsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="refunds@royalnizam.in",
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
        self.cashier = User.objects.create_user(
            email="cashier.ref@dineflow.in",
            username="cashier_ref",
            role=RoleChoices.CASHIER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.manager = User.objects.create_user(
            email="manager.ref@dineflow.in",
            username="manager_ref",
            role=RoleChoices.MANAGER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.order = Order.objects.create(
            order_number="ORD-REF-01",
            branch=self.branch,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('500.00'),
            tax_amount=Decimal('25.00'),
            grand_total=Decimal('525.00'),
            is_paid=True
        )
        self.payment = Payment.objects.create(
            order=self.order,
            amount=Decimal('525.00'),
            payment_method=PaymentMethod.UPI,
            status=PaymentStatus.SUCCESS,
            cashier=self.cashier
        )

    def test_create_refund_request_success(self):
        """Test successfully initiating a refund request within payment limits."""
        refund = create_refund_request(
            order=self.order,
            payment=self.payment,
            amount=Decimal('525.00'),
            reason="Customer cancelled before preparation started",
            requested_by=self.cashier
        )
        self.assertEqual(refund.status, RefundStatus.PENDING)
        self.assertEqual(refund.amount, Decimal('525.00'))
        self.assertTrue(refund.refund_number.startswith("REF-"))

    def test_create_refund_exceeding_payment_raises_error(self):
        """Test requesting refund amount greater than payment raises ValidationError."""
        with self.assertRaises(ValidationError):
            create_refund_request(
                order=self.order,
                payment=self.payment,
                amount=Decimal('600.00'),  # Exceeds 525.00
                reason="Invalid request",
                requested_by=self.cashier
            )

    def test_manager_approves_refund(self):
        """Test manager approves refund, updates payment status, and creates audit log."""
        refund = create_refund_request(
            order=self.order,
            payment=self.payment,
            amount=Decimal('525.00'),
            reason="Order cancellation approved",
            requested_by=self.cashier
        )
        approved = approve_refund(refund, manager=self.manager, notes="Approved full refund via UPI")
        self.assertEqual(approved.status, RefundStatus.APPROVED)
        self.assertEqual(approved.approved_by, self.manager)
        
        # Payment marked refunded
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, PaymentStatus.REFUNDED)

        # Audit log created
        log = AuditLog.objects.filter(object_id=refund.refund_number).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, AuditAction.REFUND_APPROVE)

    def test_manager_rejects_refund(self):
        """Test manager rejects refund with reason."""
        refund = create_refund_request(
            order=self.order,
            payment=self.payment,
            amount=Decimal('200.00'),
            reason="Guest requested discount post payment",
            requested_by=self.cashier
        )
        rejected = reject_refund(refund, manager=self.manager, reason="Discount cannot be applied post billing")
        self.assertEqual(rejected.status, RefundStatus.REJECTED)
        self.assertEqual(rejected.approved_by, self.manager)
        self.assertEqual(rejected.manager_notes, "Discount cannot be applied post billing")
