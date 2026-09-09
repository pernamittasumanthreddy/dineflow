"""Comprehensive Test Suite for Business Intelligence & Executive Analytics Services."""
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.menu.models import Category, MenuItem
from apps.orders.models import Order, OrderItem, OrderStatus, OrderType
from apps.expenses.models import ExpenseCategory, Expense
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.analytics.services import (
    compute_daily_snapshot,
    get_top_selling_dishes,
    get_sales_summary,
    get_payment_method_breakdown
)

class AnalyticsServicesTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="analytics@royalnizam.in",
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
        cat = Category.objects.create(restaurant=self.restaurant, name="Biryani", slug="biryani")
        self.dish1 = MenuItem.objects.create(
            category=cat, name="Chicken Biryani", code="BIR-01", base_price=Decimal('380.00')
        )
        self.dish2 = MenuItem.objects.create(
            category=cat, name="Mutton Biryani", code="BIR-02", base_price=Decimal('490.00')
        )

        # Create 2 completed orders
        self.order1 = Order.objects.create(
            order_number="ORD-AN-01",
            branch=self.branch,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('760.00'),
            tax_amount=Decimal('38.00'),
            discount_amount=Decimal('50.00'),
            grand_total=Decimal('748.00'),
            guest_count=2,
            is_paid=True
        )
        OrderItem.objects.create(order=self.order1, menu_item=self.dish1, quantity=2, unit_price=Decimal('380.00'), item_total=Decimal('760.00'))

        self.order2 = Order.objects.create(
            order_number="ORD-AN-02",
            branch=self.branch,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('490.00'),
            tax_amount=Decimal('24.50'),
            discount_amount=Decimal('0.00'),
            grand_total=Decimal('514.50'),
            guest_count=1,
            is_paid=True
        )
        OrderItem.objects.create(order=self.order2, menu_item=self.dish2, quantity=1, unit_price=Decimal('490.00'), item_total=Decimal('490.00'))

        # Payments
        Payment.objects.create(order=self.order1, amount=Decimal('748.00'), payment_method=PaymentMethod.UPI, status=PaymentStatus.SUCCESS)
        Payment.objects.create(order=self.order2, amount=Decimal('514.50'), payment_method=PaymentMethod.CASH, status=PaymentStatus.SUCCESS)

        # Expense
        exp_cat = ExpenseCategory.objects.create(name="Utilities")
        Expense.objects.create(
            branch=self.branch,
            category=exp_cat,
            title="Electricity Bill",
            amount=Decimal('300.00'),
            expense_date=timezone.localdate(),
            is_approved=True
        )

    def test_compute_daily_snapshot(self):
        """Test daily snapshot computation aggregates gross revenue, expenses, and profit."""
        snapshot = compute_daily_snapshot(self.branch)
        # Gross revenue = 748.00 + 514.50 = 1262.50
        self.assertEqual(snapshot.total_revenue, Decimal('1262.50'))
        self.assertEqual(snapshot.total_expenses, Decimal('300.00'))
        self.assertEqual(snapshot.net_profit, Decimal('962.50'))
        self.assertEqual(snapshot.order_count, 2)
        self.assertEqual(snapshot.guest_covers, 3)
        # AOV = 1262.50 / 2 = 631.25
        self.assertEqual(snapshot.average_order_value, Decimal('631.25'))

    def test_get_top_selling_dishes(self):
        """Test ranking dishes by quantity and revenue."""
        top_dishes = get_top_selling_dishes(self.branch, limit=5)
        self.assertEqual(len(top_dishes), 2)
        # Dish 1 (Chicken Biryani) revenue = 760 vs Dish 2 (Mutton Biryani) = 490
        self.assertEqual(top_dishes[0]['menu_item__code'], "BIR-01")
        self.assertEqual(top_dishes[0]['total_revenue'], Decimal('760.00'))

    def test_get_sales_summary(self):
        """Test overall sales KPI summary."""
        summary = get_sales_summary(self.branch, days=7)
        self.assertEqual(summary['total_orders'], 2)
        self.assertEqual(summary['total_revenue'], Decimal('1262.50'))
        self.assertEqual(summary['total_discounts'], Decimal('50.00'))

    def test_get_payment_method_breakdown(self):
        """Test payment method splits."""
        breakdown = get_payment_method_breakdown(self.branch, days=7)
        self.assertEqual(len(breakdown), 2)
        methods = {b['payment_method'] for b in breakdown}
        self.assertIn(PaymentMethod.UPI, methods)
        self.assertIn(PaymentMethod.CASH, methods)
