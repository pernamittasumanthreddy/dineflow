"""Comprehensive Test Suite for ESC/POS Thermal Receipt & KOT Slip Generation."""
from decimal import Decimal
from django.test import TestCase
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.tables.models import FloorSection, RestaurantTable
from apps.menu.models import Category, MenuItem
from apps.orders.models import Order, OrderItem, OrderStatus, OrderType
from apps.billing.models import Invoice, InvoiceItem
from apps.kitchen.models import KitchenTicket, KitchenStation, TicketStatus
from apps.billing.thermal import generate_thermal_receipt_text
from apps.kitchen.thermal import generate_kot_slip_text

class ThermalPrintingTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="thermal@royalnizam.in",
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
        self.section = FloorSection.objects.create(branch=self.branch, name="AC Hall")
        self.table = RestaurantTable.objects.create(
            branch=self.branch, section=self.section, table_number="T-05", seating_capacity=4
        )
        self.category = Category.objects.create(restaurant=self.restaurant, name="Biryani", slug="biryani")
        self.biryani = MenuItem.objects.create(
            category=self.category,
            name="Chicken Dum Biryani",
            code="BIR-01",
            base_price=Decimal('380.00'),
            tax_rate_percent=Decimal('5.00')
        )
        self.order = Order.objects.create(
            order_number="ORD-PRINT-01",
            order_type=OrderType.DINE_IN,
            branch=self.branch,
            table=self.table,
            status=OrderStatus.COMPLETED,
            subtotal=Decimal('380.00'),
            tax_amount=Decimal('19.00'),
            grand_total=Decimal('399.00'),
            is_paid=True
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            menu_item=self.biryani,
            quantity=1,
            unit_price=Decimal('380.00'),
            item_total=Decimal('380.00'),
            kitchen_notes="Extra raita on the side"
        )
        self.invoice = Invoice.objects.create(
            invoice_number="INV/2026-09/PRINT01",
            order=self.order,
            branch=self.branch,
            restaurant_name=self.restaurant.name,
            restaurant_gstin=self.restaurant.gstin,
            fssai_number=self.restaurant.fssai_number,
            branch_address=self.branch.address,
            taxable_subtotal=Decimal('380.00'),
            cgst_amount=Decimal('9.50'),
            sgst_amount=Decimal('9.50'),
            total_tax_amount=Decimal('19.00'),
            grand_total=Decimal('399.00'),
            is_paid=True,
            payment_method='UPI'
        )
        self.inv_item = InvoiceItem.objects.create(
            invoice=self.invoice,
            item_name="Chicken Dum Biryani",
            quantity=1,
            unit_rate=Decimal('380.00'),
            item_total=Decimal('380.00'),
            tax_rate_percent=Decimal('5.00'),
            cgst_amount=Decimal('9.50'),
            sgst_amount=Decimal('9.50')
        )
        self.kot = KitchenTicket.objects.create(
            ticket_number="KOT-PRINT-01",
            order=self.order,
            station=KitchenStation.BIRYANI_CURRY,
            status=TicketStatus.PREPARING,
            expected_prep_minutes=15
        )

    def test_thermal_receipt_formatting_80mm(self):
        """Test 80mm thermal receipt contains GSTIN, FSSAI, line items, and totals."""
        receipt = generate_thermal_receipt_text(self.invoice, width_chars=48)
        self.assertIn("The Royal Nizam", receipt)
        self.assertIn("36AAACN1234F1Z9", receipt)
        self.assertIn("13624014000189", receipt)
        self.assertIn("Chicken Dum Biryani", receipt)
        self.assertIn("CGST (2.5%):", receipt)
        self.assertIn("SGST (2.5%):", receipt)
        self.assertIn("GRAND TOTAL:", receipt)

    def test_kot_thermal_slip_formatting(self):
        """Test KOT thermal slip contains KOT #, table, station, and kitchen notes."""
        slip = generate_kot_slip_text(self.kot, width_chars=40)
        self.assertIn("KITCHEN ORDER TICKET (KOT)", slip)
        self.assertIn("KOT #: KOT-PRINT-01", slip)
        self.assertIn("TABLE: T-05", slip)
        self.assertIn("Chicken Dum Biryani", slip)
        self.assertIn("Extra raita on the side", slip)
