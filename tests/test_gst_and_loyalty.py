from decimal import Decimal
from django.test import TestCase
from apps.core.models import Restaurant, Branch
from apps.menu.models import Menu, MenuCategory, MenuItem
from apps.customers.models import Customer
from apps.loyalty.models import CustomerTier, LoyaltyAccount, LoyaltyTransaction
from apps.orders.models import Order, OrderItem
from services.billing_service import BillingService
from services.loyalty_service import LoyaltyService


class GSTAndLoyaltyTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Coastal Curry Test',
            code='CCH_TX',
            email='cch@test.com',
            phone='9440011223'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name='Chennai Central',
            code='CHN_TX',
            city='Chennai',
            state='Tamil Nadu',
            pincode='600001',
            phone='9440011223',
            email='chn@test.com'
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, name='Main Menu')
        self.cat = MenuCategory.objects.create(menu=self.menu, name='Thali', code='THALI')
        self.item = MenuItem.objects.create(category=self.cat, name='Coastal Fish Curry', base_price=Decimal('350.00'))

        self.customer = Customer.objects.create(
            restaurant=self.restaurant,
            name='Karthik Subramanian',
            phone='9840012345',
            email='karthik@test.com'
        )
        # Loyalty Tiers
        self.tier_bronze = CustomerTier.objects.create(
            restaurant=self.restaurant,
            name='Bronze',
            min_lifetime_spend=Decimal('0.00'),
            points_multiplier=Decimal('1.00')
        )
        self.tier_silver = CustomerTier.objects.create(
            restaurant=self.restaurant,
            name='Silver',
            min_lifetime_spend=Decimal('1000.00'),
            points_multiplier=Decimal('1.25')
        )

    def test_intra_state_gst_calculation(self):
        """Validates intra-state bill split into 2.5% CGST and 2.5% SGST."""
        order = Order.objects.create(
            restaurant=self.restaurant,
            branch=self.branch,
            order_number='ORD-TEST-GST-01',
            order_type='DINE_IN',
            subtotal=Decimal('700.00'),
            tax_amount=Decimal('35.00'),
            final_amount=Decimal('735.00')
        )
        OrderItem.objects.create(
            order=order,
            menu_item=self.item,
            quantity=2,
            unit_price=Decimal('350.00'),
            subtotal=Decimal('700.00'),
            total_price=Decimal('735.00')
        )

        inv = BillingService.generate_invoice_for_order(order, is_inter_state=False)

        self.assertEqual(inv.subtotal, Decimal('700.00'))
        self.assertEqual(inv.taxable_amount, Decimal('700.00'))
        # 2.5% of 700 = 17.50
        self.assertEqual(inv.cgst_amount, Decimal('17.50'))
        self.assertEqual(inv.sgst_amount, Decimal('17.50'))
        self.assertEqual(inv.igst_amount, Decimal('0.00'))
        self.assertEqual(inv.grand_total, Decimal('735.00'))

    def test_inter_state_gst_calculation(self):
        """Validates inter-state bill charged at 5% IGST."""
        order = Order.objects.create(
            restaurant=self.restaurant,
            branch=self.branch,
            order_number='ORD-TEST-GST-02',
            order_type='DELIVERY',
            subtotal=Decimal('1000.00'),
            tax_amount=Decimal('50.00'),
            final_amount=Decimal('1050.00')
        )
        OrderItem.objects.create(
            order=order,
            menu_item=self.item,
            quantity=2,
            unit_price=Decimal('500.00'),
            subtotal=Decimal('1000.00'),
            total_price=Decimal('1050.00')
        )

        inv = BillingService.generate_invoice_for_order(order, is_inter_state=True)

        self.assertEqual(inv.cgst_amount, Decimal('0.00'))
        self.assertEqual(inv.sgst_amount, Decimal('0.00'))
        self.assertEqual(inv.igst_amount, Decimal('50.00'))
        self.assertEqual(inv.grand_total, Decimal('1050.00'))

    def test_loyalty_point_accrual_and_tier_upgrade(self):
        """Validates loyalty point earning and automatic tier advancement."""
        account = LoyaltyService.get_or_create_loyalty_account(self.customer)
        self.assertEqual(account.tier.name, 'Bronze')

        # Bill of ₹1200 should earn points and advance to Silver (spend >= 1000)
        order = Order.objects.create(
            restaurant=self.restaurant,
            branch=self.branch,
            customer=self.customer,
            order_number='ORD-LOYALTY-01',
            order_type='DINE_IN',
            subtotal=Decimal('1200.00'),
            final_amount=Decimal('1260.00')
        )

        LoyaltyService.process_order_loyalty(order)
        account.refresh_from_db()
        self.customer.refresh_from_db()

        # Base 5% of 1260 = 63 points
        self.assertEqual(account.current_points, Decimal('63.00'))
        self.assertEqual(self.customer.total_spend, Decimal('1260.00'))
        # Tier upgraded to Silver!
        self.assertEqual(account.tier.name, 'Silver')

        # Auditable transaction created
        tx = LoyaltyTransaction.objects.filter(account=account).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.transaction_type, 'EARNED')
        self.assertEqual(tx.points, Decimal('63.00'))
