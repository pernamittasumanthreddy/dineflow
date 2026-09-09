"""Comprehensive Test Suite for Inventory, BOM Recipe Deductions, and Stock Ledgers."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.inventory.models import IngredientCategory, Ingredient, StockMovement, MovementType
from apps.menu.models import Category, MenuItem, RecipeItem, FoodType
from apps.suppliers.models import Supplier
from apps.purchases.models import PurchaseOrder, PurchaseOrderItem, POStatus

User = get_user_model()

class InventoryAndBOMTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="inventory@royalnizam.in",
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
        self.inventory_manager = User.objects.create_user(
            email="inventory.mgr@dineflow.in",
            username="inv_mgr",
            role=RoleChoices.INVENTORY_MANAGER,
            branch=self.branch,
            restaurant=self.restaurant
        )
        self.category_grain = IngredientCategory.objects.create(
            name="Grains & Rice",
            description="Basmati, Biryani rice, whole wheat"
        )
        self.rice = Ingredient.objects.create(
            branch=self.branch,
            category=self.category_grain,
            name="Aged Daawat Basmati Rice",
            code="ING-RIC-01",
            unit="kg",
            current_stock=Decimal('100.000'),
            minimum_stock_level=Decimal('25.000'),
            optimal_stock_level=Decimal('200.000'),
            unit_cost=Decimal('120.00')
        )
        self.category_poultry = IngredientCategory.objects.create(
            name="Poultry & Meat",
            description="Fresh farm chicken and mutton"
        )
        self.chicken = Ingredient.objects.create(
            branch=self.branch,
            category=self.category_poultry,
            name="Tender Country Chicken",
            code="ING-CHK-01",
            unit="kg",
            current_stock=Decimal('20.000'),  # Under low stock threshold of 25.000
            minimum_stock_level=Decimal('25.000'),
            optimal_stock_level=Decimal('100.000'),
            unit_cost=Decimal('220.00')
        )

    def test_low_stock_detection(self):
        """Test is_low_stock property flags ingredients when stock drops to or below reorder level."""
        self.assertFalse(self.rice.is_low_stock)
        self.assertTrue(self.chicken.is_low_stock)

    def test_stock_valuation(self):
        """Test total monetary value of current warehouse inventory."""
        # 100 kg * 120 = 12,000 INR
        self.assertEqual(self.rice.stock_value, Decimal('12000.00'))
        # 20 kg * 220 = 4,400 INR
        self.assertEqual(self.chicken.stock_value, Decimal('4400.00'))

    def test_bill_of_materials_bom_linkage(self):
        """Test linking raw ingredients to culinary dishes via RecipeItem."""
        m_cat = Category.objects.create(restaurant=self.restaurant, name="Biryani", slug="biryani")
        dish = MenuItem.objects.create(
            category=m_cat,
            name="Dum Biryani Portioned",
            code="BIR-01",
            food_type=FoodType.NON_VEG,
            base_price=Decimal('350.00')
        )
        # Recipe: 350g rice + 300g chicken
        recipe_rice = RecipeItem.objects.create(
            menu_item=dish,
            ingredient=self.rice,
            ingredient_name=self.rice.name,
            quantity_required=Decimal('0.350'),
            unit="kg"
        )
        recipe_chk = RecipeItem.objects.create(
            menu_item=dish,
            ingredient=self.chicken,
            ingredient_name=self.chicken.name,
            quantity_required=Decimal('0.300'),
            unit="kg"
        )
        self.assertEqual(dish.recipe_ingredients.count(), 2)
        self.assertEqual(recipe_rice.quantity_required, Decimal('0.350'))

    def test_stock_movement_audit_ledger(self):
        """Test immutable stock movement transaction logging."""
        initial_stock = self.rice.current_stock
        delta = Decimal('-15.500')  # Consumed for batch prep
        new_stock = initial_stock + delta

        movement = StockMovement.objects.create(
            ingredient=self.rice,
            movement_type=MovementType.ORDER_CONSUMPTION,
            quantity=delta,
            stock_before=initial_stock,
            stock_after=new_stock,
            reference_id="BATCH-20260909-01",
            recorded_by=self.inventory_manager,
            notes="Lunch service biryani batch preparation"
        )
        self.rice.current_stock = new_stock
        self.rice.save()

        self.assertEqual(self.rice.current_stock, Decimal('84.500'))
        self.assertEqual(movement.movement_type, MovementType.ORDER_CONSUMPTION)
        self.assertEqual(movement.stock_after, Decimal('84.500'))

    def test_purchase_order_inward_goods(self):
        """Test raising a purchase order and receiving goods inward."""
        supplier = Supplier.objects.create(
            company_name="Deccan Grain Co.",
            contact_person="Syed Mansoor",
            phone="+91 40 2456 8900",
            address="Begum Bazaar, Hyderabad",
            city="Hyderabad"
        )
        po = PurchaseOrder.objects.create(
            po_number="PO-20260909-001",
            supplier=supplier,
            branch=self.branch,
            order_date="2026-09-09",
            status=POStatus.APPROVED,
            created_by=self.inventory_manager
        )
        po_item = PurchaseOrderItem.objects.create(
            purchase_order=po,
            ingredient=self.rice,
            ordered_quantity=Decimal('50.000'),
            unit_cost=Decimal('115.00'),
            gst_rate_percent=Decimal('5.00'),
            item_total=Decimal('5750.00'),
            gst_amount=Decimal('287.50')
        )
        po.recalculate_totals()
        self.assertEqual(po.subtotal, Decimal('5750.00'))
        self.assertEqual(po.gst_amount, Decimal('287.50'))
        self.assertEqual(po.total_amount, Decimal('6037.50'))
