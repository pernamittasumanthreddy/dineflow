"""Comprehensive Test Suite for Home Delivery Logistics and Operational Expenses."""
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.orders.models import Order, OrderStatus, OrderType
from apps.delivery.models import DeliveryOrder, DeliveryStatus
from apps.expenses.models import ExpenseCategory, Expense

User = get_user_model()

class DeliveryAndExpensesTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="dispatch@royalnizam.in",
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
            email="mgr@dineflow.in",
            username="mgr_dispatch",
            role=RoleChoices.MANAGER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.rider = User.objects.create_user(
            email="rider@dineflow.in",
            username="rider_arun",
            role=RoleChoices.WAITER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.order = Order.objects.create(
            order_number="ORD-DEL-001",
            order_type=OrderType.DELIVERY,
            branch=self.branch,
            server=self.manager,
            status=OrderStatus.CONFIRMED,
            subtotal=Decimal('650.00'),
            tax_amount=Decimal('32.50'),
            grand_total=Decimal('682.50')
        )

    def test_delivery_order_lifecycle(self):
        """Test delivery order creation, rider assignment, and delivery progression."""
        delivery = DeliveryOrder.objects.create(
            order=self.order,
            recipient_name="Vikram Varma",
            recipient_phone="+91 98765 43210",
            delivery_address="Flat 402, Nizam Heights, Banjara Hills",
            pincode="500034",
            landmark="Near City Center Mall",
            status=DeliveryStatus.PENDING_RIDER,
            estimated_delivery_minutes=30
        )
        self.assertEqual(delivery.status, DeliveryStatus.PENDING_RIDER)

        # Rider is assigned
        delivery.assigned_rider = self.rider
        delivery.status = DeliveryStatus.ASSIGNED
        delivery.save()
        self.assertEqual(delivery.assigned_rider.username, "rider_arun")

        # Picked up from kitchen
        delivery.status = DeliveryStatus.PICKED_UP
        delivery.dispatched_at = timezone.now()
        delivery.save()
        self.assertEqual(delivery.status, DeliveryStatus.PICKED_UP)

        # Out for delivery & Delivered
        delivery.status = DeliveryStatus.DELIVERED
        delivery.delivered_at = timezone.now()
        delivery.save()
        self.assertEqual(delivery.status, DeliveryStatus.DELIVERED)

    def test_operational_expense_creation_and_approval(self):
        """Test branch operating expense voucher submission and manager signoff."""
        cat_gas = ExpenseCategory.objects.create(
            name="LPG Cylinder Gas",
            description="Commercial cylinders for cooking ranges"
        )
        expense = Expense.objects.create(
            branch=self.branch,
            category=cat_gas,
            title="Commercial Indane LPG 19kg (3x Refills)",
            amount=Decimal('5400.00'),
            expense_date=timezone.localdate(),
            payment_mode='CASH',
            requested_by=self.rider,
            notes="Refills for Biryani Dum Range"
        )
        self.assertFalse(expense.is_approved)

        # Manager approves expense
        expense.is_approved = True
        expense.approved_by = self.manager
        expense.save()

        self.assertTrue(expense.is_approved)
        self.assertEqual(expense.approved_by.username, "mgr_dispatch")
        self.assertEqual(expense.amount, Decimal('5400.00'))
