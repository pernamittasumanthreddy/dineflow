"""Comprehensive Test Suite for Custom QuerySets, Managers, and Query Optimizations."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.tables.models import FloorSection, RestaurantTable
from apps.menu.models import Category, MenuItem
from apps.orders.models import Order, OrderItem, OrderStatus, OrderType
from apps.billing.models import Invoice, InvoiceItem
from apps.inventory.models import IngredientCategory, Ingredient

User = get_user_model()

class QueryOptimizationTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="query@royalnizam.in",
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
        self.section = FloorSection.objects.create(branch=self.branch, name="Hall")
        self.table = RestaurantTable.objects.create(
            branch=self.branch, section=self.section, table_number="T-01"
        )
        self.category = Category.objects.create(restaurant=self.restaurant, name="Rice", slug="rice")
        self.dish = MenuItem.objects.create(
            category=self.category, name="Fried Rice", code="RIC-01", base_price=Decimal('200.00')
        )
        self.order_active = Order.objects.create(
            order_number="ORD-OPT-01",
            branch=self.branch,
            table=self.table,
            status=OrderStatus.PREPARING,
            subtotal=Decimal('200.00')
        )
        self.order_done = Order.objects.create(
            order_number="ORD-OPT-02",
            branch=self.branch,
            table=self.table,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('200.00')
        )
        OrderItem.objects.create(order=self.order_active, menu_item=self.dish, quantity=1, unit_price=Decimal('200.00'), item_total=Decimal('200.00'))

        self.invoice = Invoice.objects.create(
            invoice_number="INV/OPT/01",
            order=self.order_done,
            branch=self.branch,
            taxable_subtotal=Decimal('200.00'),
            grand_total=Decimal('210.00')
        )
        InvoiceItem.objects.create(
            invoice=self.invoice, item_name="Fried Rice", unit_rate=Decimal('200.00'), item_total=Decimal('200.00')
        )

        ing_cat = IngredientCategory.objects.create(name="Grains")
        self.ing_normal = Ingredient.objects.create(
            branch=self.branch, category=ing_cat, name="Rice Normal", current_stock=Decimal('50.000'), minimum_stock_level=Decimal('20.000')
        )
        self.ing_low = Ingredient.objects.create(
            branch=self.branch, category=ing_cat, name="Rice Low", current_stock=Decimal('10.000'), minimum_stock_level=Decimal('20.000')
        )

    def test_order_queryset_active_orders(self):
        """Test Order.objects.active_orders() filters out completed and cancelled orders."""
        active = Order.objects.active_orders()
        self.assertIn(self.order_active, active)
        self.assertNotIn(self.order_done, active)

    def test_order_queryset_with_details(self):
        """Test Order.objects.with_details() executes prefetch without error."""
        orders = list(Order.objects.with_details())
        self.assertEqual(len(orders), 2)
        # Check pre-fetched relations
        self.assertEqual(orders[0].table.table_number, "T-01")

    def test_invoice_queryset_with_details(self):
        """Test Invoice.objects.with_details() prefetches invoice items."""
        invoices = list(Invoice.objects.with_details())
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoices[0].items.count(), 1)

    def test_ingredient_queryset_low_stock(self):
        """Test Ingredient.objects.low_stock() filters for low stock records."""
        low_items = list(Ingredient.objects.low_stock())
        self.assertEqual(len(low_items), 1)
        self.assertEqual(low_items[0].name, "Rice Low")
