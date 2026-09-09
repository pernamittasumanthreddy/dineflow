from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from apps.core.models import Restaurant, Branch
from apps.inventory.models import Unit, InventoryCategory, InventoryItem, Stock, StockMovement
from apps.menu.models import Menu, MenuCategory, MenuItem, Recipe, FoodIngredient
from apps.orders.models import Order
from apps.billing.models import InvoiceNumberSequence
from services.order_service import OrderService
from services.billing_service import BillingService


class DatabaseTransactionsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Hyderabad Biryani Hub Test',
            legal_name='HBH Pvt Ltd',
            code='HBH_TX',
            email='tx@hbh.com',
            phone='9848011223'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name='Banjara Hills',
            code='HYD_TX',
            city='Hyderabad',
            state='Telangana',
            pincode='500034',
            phone='9848011223',
            email='hyd@hbh.com'
        )
        self.unit_kg = Unit.objects.create(name='Kilogram', symbol='kg_tx', is_base_unit=True)
        self.inv_cat = InventoryCategory.objects.create(restaurant=self.restaurant, name='Grains', code='GRAINS_TX')

        # Raw ingredients
        self.rice = InventoryItem.objects.create(
            restaurant=self.restaurant,
            category=self.inv_cat,
            name='Basmati Rice',
            item_code='RICE_TX',
            primary_unit=self.unit_kg,
            reorder_level=Decimal('10.000'),
            current_cost_per_unit=Decimal('90.00')
        )
        self.chicken = InventoryItem.objects.create(
            restaurant=self.restaurant,
            category=self.inv_cat,
            name='Chicken',
            item_code='CHICK_TX',
            primary_unit=self.unit_kg,
            reorder_level=Decimal('10.000'),
            current_cost_per_unit=Decimal('180.00')
        )

        # Initial stock: 50 kg rice, 50 kg chicken
        Stock.objects.create(
            branch=self.branch,
            inventory_item=self.rice,
            quantity_on_hand=Decimal('50.000'),
            available_quantity=Decimal('50.000')
        )
        Stock.objects.create(
            branch=self.branch,
            inventory_item=self.chicken,
            quantity_on_hand=Decimal('50.000'),
            available_quantity=Decimal('50.000')
        )

        # Menu Item & Recipe BOM
        self.menu = Menu.objects.create(restaurant=self.restaurant, name='Biryani Menu')
        self.cat = MenuCategory.objects.create(menu=self.menu, name='Dum Biryani', code='DUM_TX')
        self.biryani = MenuItem.objects.create(
            category=self.cat,
            name='Special Chicken Biryani',
            base_price=Decimal('300.00'),
            is_available=True
        )

        self.recipe = Recipe.objects.create(
            menu_item=self.biryani,
            title='Dum Chicken Biryani Recipe',
            instructions='Cook on dum'
        )
        # 1 biryani requires 0.25 kg rice and 0.30 kg chicken
        FoodIngredient.objects.create(
            recipe=self.recipe,
            inventory_item=self.rice,
            quantity_required=Decimal('0.250'),
            unit_name='kg'
        )
        FoodIngredient.objects.create(
            recipe=self.recipe,
            inventory_item=self.chicken,
            quantity_required=Decimal('0.300'),
            unit_name='kg'
        )

    def test_order_placement_and_kot_generation(self):
        """Validates placing an order atomically creates items, KOT, and updates totals."""
        order = OrderService.place_order(
            branch=self.branch,
            order_type='DINE_IN',
            items_data=[{'menu_item': self.biryani, 'quantity': 2}],
            notes='Table 1'
        )
        self.assertEqual(order.status, 'PLACED')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.kitchen_orders.count(), 1)
        # 2 x 300 = 600 subtotal, + 5% GST = 630.00
        self.assertEqual(order.subtotal, Decimal('600.00'))
        self.assertEqual(order.tax_amount, Decimal('30.00'))
        self.assertEqual(order.final_amount, Decimal('630.00'))

    def test_recipe_bom_inventory_deduction_on_order_transition(self):
        """Validates that advancing order to PREPARING accurately deducts stock and records movements."""
        order = OrderService.place_order(
            branch=self.branch,
            order_type='DINE_IN',
            items_data=[{'menu_item': self.biryani, 'quantity': 4}],  # 4 biryanis
        )

        # Transition order to PREPARING
        OrderService.transition_order_status(order, 'PREPARING')

        # Check stock:
        # Rice: 50.000 - (4 * 0.250) = 49.000
        # Chicken: 50.000 - (4 * 0.300) = 48.800
        rice_stock = Stock.objects.get(branch=self.branch, inventory_item=self.rice)
        chicken_stock = Stock.objects.get(branch=self.branch, inventory_item=self.chicken)

        self.assertEqual(rice_stock.quantity_on_hand, Decimal('49.000'))
        self.assertEqual(chicken_stock.quantity_on_hand, Decimal('48.800'))

        # Check traceable stock movements
        movements = StockMovement.objects.filter(reference_id=f"ORDER #{order.order_number}")
        self.assertEqual(movements.count(), 2)
        rice_move = movements.get(inventory_item=self.rice)
        self.assertEqual(rice_move.movement_type, 'RECIPE_CONSUMPTION')
        self.assertEqual(rice_move.quantity, Decimal('-1.000'))
        self.assertEqual(rice_move.balance_after, Decimal('49.000'))

    def test_invoice_sequence_generation_uniqueness(self):
        """Validates sequential atomic invoice numbering without gaps."""
        order1 = OrderService.place_order(
            branch=self.branch,
            order_type='TAKEAWAY',
            items_data=[{'menu_item': self.biryani, 'quantity': 1}],
        )
        order2 = OrderService.place_order(
            branch=self.branch,
            order_type='TAKEAWAY',
            items_data=[{'menu_item': self.biryani, 'quantity': 1}],
        )

        inv1 = BillingService.generate_invoice_for_order(order1)
        inv2 = BillingService.generate_invoice_for_order(order2)

        self.assertTrue(inv1.invoice_number.endswith('/00001'))
        self.assertTrue(inv2.invoice_number.endswith('/00002'))
        self.assertNotEqual(inv1.invoice_number, inv2.invoice_number)
