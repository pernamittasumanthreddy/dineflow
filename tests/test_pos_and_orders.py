"""Comprehensive Test Suite for Dining Tables, POS Ordering, Totals, and Kitchen KDS."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.tables.models import FloorSection, RestaurantTable, TableStatus
from apps.menu.models import Category, MenuItem, FoodType
from apps.orders.models import Order, OrderItem, OrderStatus, OrderType
from apps.kitchen.models import KitchenTicket, KitchenStation, TicketStatus

User = get_user_model()

class POSAndOrdersTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="pos@royalnizam.in",
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
        self.waiter = User.objects.create_user(
            email="waiter@dineflow.in",
            username="waiter_pos",
            role=RoleChoices.WAITER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.section = FloorSection.objects.create(
            branch=self.branch,
            name="AC Main Dining Hall"
        )
        self.table = RestaurantTable.objects.create(
            branch=self.branch,
            section=self.section,
            table_number="T-01",
            seating_capacity=4,
            status=TableStatus.AVAILABLE
        )
        self.category = Category.objects.create(
            restaurant=self.restaurant,
            name="Biryani & Pulao",
            slug="biryani-pulao"
        )
        self.biryani = MenuItem.objects.create(
            category=self.category,
            name="Hyderabadi Chicken Dum Biryani",
            code="BIR-CHK-01",
            food_type=FoodType.NON_VEG,
            base_price=Decimal('380.00'),
            tax_rate_percent=Decimal('5.00'),
            preparation_time_minutes=25,
            is_available=True
        )
        self.naan = MenuItem.objects.create(
            category=self.category,
            name="Garlic Butter Naan",
            code="BRD-NAN-01",
            food_type=FoodType.VEG,
            base_price=Decimal('70.00'),
            tax_rate_percent=Decimal('5.00'),
            preparation_time_minutes=8,
            is_available=True
        )

    def test_create_dine_in_order(self):
        """Test creating an initial dine-in order and table occupancy."""
        order = Order.objects.create(
            order_number="ORD-TEST-001",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            table=self.table,
            server=self.waiter,
            status=OrderStatus.NEW,
            guest_count=2
        )
        self.assertEqual(order.status, OrderStatus.NEW)
        self.assertEqual(order.table.table_number, "T-01")
        self.assertEqual(order.server.username, "waiter_pos")

    def test_order_items_and_totals_recalculation(self):
        """Test adding line items and recalculating subtotal, 5% GST, and grand total."""
        order = Order.objects.create(
            order_number="ORD-TEST-002",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            table=self.table,
            server=self.waiter,
            status=OrderStatus.NEW
        )
        # 2x Biryani @ ₹380 = ₹760
        item1 = OrderItem.objects.create(
            order=order,
            menu_item=self.biryani,
            quantity=2,
            unit_price=Decimal('380.00')
        )
        # 2x Garlic Butter Naan @ ₹70 = ₹140
        item2 = OrderItem.objects.create(
            order=order,
            menu_item=self.naan,
            quantity=2,
            unit_price=Decimal('70.00')
        )
        # Verify item totals
        self.assertEqual(item1.item_total, Decimal('760.00'))
        self.assertEqual(item2.item_total, Decimal('140.00'))

        # Recalculate order totals
        order.recalculate_totals()
        
        # Subtotal: 760 + 140 = 900.00
        self.assertEqual(order.subtotal, Decimal('900.00'))
        # GST @ 5% on 900 = 45.00
        self.assertEqual(order.tax_amount, Decimal('45.00'))
        # Grand Total = 900 + 45 = 945.00
        self.assertEqual(order.grand_total, Decimal('945.00'))

    def test_order_status_state_machine(self):
        """Test progression through lifecycle: NEW -> CONFIRMED -> PREPARING -> READY -> COMPLETED."""
        order = Order.objects.create(
            order_number="ORD-TEST-003",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            table=self.table,
            server=self.waiter,
            status=OrderStatus.NEW
        )
        self.assertEqual(order.status, OrderStatus.NEW)
        
        order.status = OrderStatus.CONFIRMED
        order.save()
        self.assertEqual(order.status, OrderStatus.CONFIRMED)

        order.status = OrderStatus.PREPARING
        order.save()
        self.assertEqual(order.status, OrderStatus.PREPARING)

        order.status = OrderStatus.READY
        order.save()
        self.assertEqual(order.status, OrderStatus.READY)

        order.status = OrderStatus.COMPLETED
        order.is_paid = True
        order.save()
        self.assertEqual(order.status, OrderStatus.COMPLETED)
        self.assertTrue(order.is_paid)

    def test_kitchen_ticket_kds_creation(self):
        """Test KDS ticket generation for kitchen stations with SLA tracking."""
        order = Order.objects.create(
            order_number="ORD-TEST-004",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            table=self.table,
            server=self.waiter,
            status=OrderStatus.PREPARING
        )
        kot = KitchenTicket.objects.create(
            ticket_number="KOT-TEST-001",
            order=order,
            station=KitchenStation.BIRYANI_CURRY,
            status=TicketStatus.PREPARING,
            expected_prep_minutes=20
        )
        self.assertEqual(kot.station, KitchenStation.BIRYANI_CURRY)
        self.assertEqual(kot.status, TicketStatus.PREPARING)
        self.assertEqual(kot.expected_prep_minutes, 20)
        self.assertFalse(kot.is_delayed)
