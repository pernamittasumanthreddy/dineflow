from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.core.models import Branch, Restaurant
from apps.inventory.models import InventoryCategory, InventoryItem, Stock, Unit
from apps.menu.models import Menu, MenuCategory, MenuItem
from apps.tables.models import RestaurantTable, TableSection


class DatabaseConstraintsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Andhra Kitchen',
            legal_name='Test Andhra Kitchen Ltd',
            code='TAK_TEST',
            email='test@andhra.com',
            phone='9988776655'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name='Guntur Main',
            code='GNT01',
            city='Guntur',
            state='Andhra Pradesh',
            pincode='522002',
            phone='9988776655',
            email='gnt@andhra.com'
        )
        self.unit_kg = Unit.objects.create(name='Kilogram', symbol='kg_t', is_base_unit=True)
        self.category = InventoryCategory.objects.create(
            restaurant=self.restaurant,
            name='Grains',
            code='GRAINS'
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, name='Dine-in Menu')
        self.menu_cat = MenuCategory.objects.create(menu=self.menu, name='Biryani', code='BIRYANI')

    def test_menu_item_positive_price_constraint(self):
        """Validates that base_price cannot be negative."""
        with self.assertRaises(IntegrityError):
            MenuItem.objects.create(
                category=self.menu_cat,
                name='Illegal Price Item',
                base_price=Decimal('-50.00'),
            )

    def test_stock_quantity_non_negative_constraint(self):
        """Validates that stock quantity on hand cannot be negative."""
        inv_item = InventoryItem.objects.create(
            restaurant=self.restaurant,
            category=self.category,
            name='Basmati Rice',
            item_code='RICE_01',
            primary_unit=self.unit_kg,
            reorder_level=Decimal('10.000'),
            current_cost_per_unit=Decimal('90.00')
        )
        with self.assertRaises(IntegrityError):
            Stock.objects.create(
                branch=self.branch,
                inventory_item=inv_item,
                quantity_on_hand=Decimal('-5.000'),
                available_quantity=Decimal('-5.000')
            )

    def test_unique_branch_code_per_restaurant(self):
        """Validates unique branch code within the same restaurant."""
        with self.assertRaises(IntegrityError):
            Branch.objects.create(
                restaurant=self.restaurant,
                name='Duplicate Branch Code',
                code='GNT01',  # Same code for same restaurant
                city='Guntur',
                state='Andhra Pradesh',
                pincode='522002',
                phone='9988776655',
                email='dup@andhra.com'
            )

    def test_table_seating_capacity_positive_constraint(self):
        """Validates seating capacity must be strictly greater than 0."""
        sec = TableSection.objects.create(branch=self.branch, name='AC Hall')
        with self.assertRaises(IntegrityError):
            RestaurantTable.objects.create(
                branch=self.branch,
                section=sec,
                table_number='T-INVALID',
                seating_capacity=0,
                min_capacity=0
            )

    def test_table_capacity_gte_min_capacity_constraint(self):
        """Validates that seating_capacity cannot be less than min_capacity."""
        sec = TableSection.objects.create(branch=self.branch, name='AC Hall 2')
        with self.assertRaises(IntegrityError):
            RestaurantTable.objects.create(
                branch=self.branch,
                section=sec,
                table_number='T-INVALID2',
                seating_capacity=2,
                min_capacity=4  # seating_capacity < min_capacity
            )
