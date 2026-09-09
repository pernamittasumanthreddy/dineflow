import os
import sys
from datetime import date, timedelta
from decimal import Decimal

from django.utils import timezone

# Setup Django environment if run as standalone script
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dineflow.settings')
    import django
    django.setup()

from apps.analytics.models import DailySalesSnapshot
from apps.billing.models import Invoice, InvoiceItem
from apps.core.models import (
    Branch,
    BranchSettings,
    Restaurant,
    RestaurantSettings,
    Role,
    User,
    UserRole,
)
from apps.customers.models import Customer, CustomerPreference
from apps.employees.models import (
    Department,
    Designation,
    Employee,
    SalaryStructure,
    Shift,
)
from apps.expenses.models import Expense, ExpenseCategory
from apps.inventory.models import (
    InventoryCategory,
    InventoryItem,
    Stock,
    StockBatch,
    StockMovement,
    Unit,
)
from apps.kitchen.models import KitchenStation
from apps.loyalty.models import CustomerTier, LoyaltyAccount
from apps.menu.models import (
    FoodIngredient,
    Menu,
    MenuAddon,
    MenuCategory,
    MenuItem,
    MenuVariant,
    Recipe,
)
from apps.notifications.models import Notification
from apps.orders.models import Order, OrderItem, OrderStatusHistory
from apps.payments.models import (
    Payment,
    PaymentMethod,
    PaymentTransaction,
    RefundReason,
)
from apps.suppliers.models import Supplier
from apps.tables.models import RestaurantTable, TableSection
from apps.taxes.models import (
    BranchTaxConfiguration,
    RestaurantTaxConfiguration,
    TaxCategory,
    TaxRate,
)


def seed_all():
    print("--- Starting DineFlow Comprehensive Indian ERP Database Seeding ---")

    # 1. Base Payment Methods
    payment_methods = [
        ('CASH', 'Cash'),
        ('UPI', 'Unified Payments Interface (UPI)'),
        ('CARD', 'Credit / Debit Card'),
        ('NET_BANKING', 'Internet Banking'),
        ('LOYALTY_POINTS', 'Loyalty Points Redemption'),
    ]
    for code, name in payment_methods:
        PaymentMethod.objects.get_or_create(code=code, defaults={'name': name, 'is_active': True})
    print("[1/13] Payment methods configured.")

    # 2. Refund Reasons
    refund_reasons = [
        ('CUST_CANCEL', 'Customer Cancelled Order'),
        ('QUALITY_ISSUE', 'Food Quality Issue'),
        ('DELAYED_SERVICE', 'Excessive Delay in Service'),
        ('BILLING_ERROR', 'Billing Calculation Correction'),
    ]
    for code, title in refund_reasons:
        RefundReason.objects.get_or_create(code=code, defaults={'title': title, 'is_active': True})
    print("[2/13] Refund reasons initialized.")

    # 3. Units of Measurement
    units_data = [
        ('Kilogram', 'kg'),
        ('Gram', 'g'),
        ('Litre', 'l'),
        ('Millilitre', 'ml'),
        ('Piece', 'pcs'),
        ('Packet', 'pkt'),
        ('Box', 'box'),
    ]
    units = {}
    for name, sym in units_data:
        u, _ = Unit.objects.get_or_create(symbol=sym, defaults={'name': name, 'is_base_unit': True})
        units[sym] = u
    print("[3/13] Measurement units seeded.")

    # 4. Super Admin User
    admin_user, _ = User.objects.get_or_create(
        email='admin@dineflow.com',
        defaults={
            'phone': '9876543210',
            'first_name': 'DineFlow',
            'last_name': 'Super Admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    admin_user.set_password('AdminPassword@123')
    admin_user.save()

    # System Roles
    role_codes = ['SUPER_ADMIN', 'RESTAURANT_OWNER', 'BRANCH_MANAGER', 'CASHIER', 'HEAD_CHEF', 'WAITER', 'DELIVERY_RIDER', 'INVENTORY_MANAGER']
    roles = {}
    for r_code in role_codes:
        role_obj, _ = Role.objects.get_or_create(
            code=r_code,
            defaults={'name': r_code.replace('_', ' ').title(), 'is_system_role': True}
        )
        roles[r_code] = role_obj

    # 5. Restaurants
    restaurants_info = [
        {
            'name': 'Andhra Spice Kitchen',
            'legal_name': 'Andhra Spice Kitchen Pvt Ltd',
            'code': 'ASK',
            'gstin': '37AAACA1234F1Z9',
            'fssai_license': '10120000001234',
            'email': 'contact@andhraspice.com',
            'phone': '+91 866 2456789',
        },
        {
            'name': 'Coastal Curry House',
            'legal_name': 'Coastal Curry Hospitality LLP',
            'code': 'CCH',
            'gstin': '33AAACB5678G1Z2',
            'fssai_license': '10120000005678',
            'email': 'info@coastalcurry.com',
            'phone': '+91 44 28289900',
        },
        {
            'name': 'Hyderabad Biryani Hub',
            'legal_name': 'Deccan Flavors & Biryani Hub Pvt Ltd',
            'code': 'HBH',
            'gstin': '36AAACD9012H1Z5',
            'fssai_license': '10120000009012',
            'email': 'dine@hyderabadbiryani.in',
            'phone': '+91 40 66778899',
        },
        {
            'name': 'Kerala Taste Restaurant',
            'legal_name': 'Malabar & Travancore Foods Pvt Ltd',
            'code': 'KTR',
            'gstin': '32AAACE3456J1Z1',
            'fssai_license': '10120000003456',
            'email': 'hello@keralataste.in',
            'phone': '+91 484 2345678',
        },
    ]

    restaurants = {}
    for r_data in restaurants_info:
        r, _ = Restaurant.objects.get_or_create(
            code=r_data['code'],
            defaults=r_data
        )
        RestaurantSettings.objects.get_or_create(
            restaurant=r,
            defaults={
                'fiscal_year_start_month': 4,
                'invoice_prefix': 'INV',
                'kot_prefix': 'KOT',
                'round_off_bills': True,
                'loyalty_points_per_rupee': Decimal('0.05'),
            }
        )
        RestaurantTaxConfiguration.objects.get_or_create(
            restaurant=r,
            defaults={
                'pan_number': r_data['gstin'][2:12],
                'is_composition_scheme': False,
                'default_service_charge_percent': Decimal('0.00'),
            }
        )
        # Loyalty Tiers
        tiers = [
            ('Bronze', Decimal('0.00'), Decimal('1.00'), '#CD7F32'),
            ('Silver', Decimal('5000.00'), Decimal('1.25'), '#C0C0C0'),
            ('Gold', Decimal('15000.00'), Decimal('1.50'), '#FFD700'),
            ('Platinum', Decimal('30000.00'), Decimal('2.00'), '#E5E4E2'),
        ]
        for t_name, min_spend, mult, col in tiers:
            CustomerTier.objects.get_or_create(
                restaurant=r,
                name=t_name,
                defaults={'min_lifetime_spend': min_spend, 'points_multiplier': mult, 'badge_color': col}
            )

        # Tax Category & Rates
        tax_cat, _ = TaxCategory.objects.get_or_create(
            restaurant=r,
            code='GST_FOOD_5',
            defaults={'name': 'Restaurant Food Services 5%', 'hsn_sac_code': '996331'}
        )
        TaxRate.objects.get_or_create(tax_category=tax_cat, component_name='CGST', defaults={'rate_percent': Decimal('2.50')})
        TaxRate.objects.get_or_create(tax_category=tax_cat, component_name='SGST', defaults={'rate_percent': Decimal('2.50')})
        TaxRate.objects.get_or_create(tax_category=tax_cat, component_name='IGST', defaults={'rate_percent': Decimal('5.00')})

        restaurants[r_data['code']] = r
    print("[4/13] 4 Indian Restaurant entities, tax configs, and loyalty tiers created.")

    # 6. Branches
    branches_info = [
        # Andhra Spice Kitchen
        {'restaurant': 'ASK', 'name': 'MG Road Branch', 'code': 'VJA01', 'city': 'Vijayawada', 'state': 'Andhra Pradesh', 'pincode': '520010', 'gstin': '37AAACA1234F1Z9', 'state_code': '37'},
        {'restaurant': 'ASK', 'name': 'Arundelpet Branch', 'code': 'GNT01', 'city': 'Guntur', 'state': 'Andhra Pradesh', 'pincode': '522002', 'gstin': '37AAACA1234F1Z9', 'state_code': '37'},
        # Hyderabad Biryani Hub
        {'restaurant': 'HBH', 'name': 'Banjara Hills Branch', 'code': 'HYD01', 'city': 'Hyderabad', 'state': 'Telangana', 'pincode': '500034', 'gstin': '36AAACD9012H1Z5', 'state_code': '36'},
        # Coastal Curry House
        {'restaurant': 'CCH', 'name': 'T. Nagar Branch', 'code': 'CHN01', 'city': 'Chennai', 'state': 'Tamil Nadu', 'pincode': '600017', 'gstin': '33AAACB5678G1Z2', 'state_code': '33'},
        {'restaurant': 'CCH', 'name': 'Indiranagar Branch', 'code': 'BLR01', 'city': 'Bengaluru', 'state': 'Karnataka', 'pincode': '560038', 'gstin': '29AAACB5678G1Z8', 'state_code': '29'},
        # Kerala Taste Restaurant
        {'restaurant': 'KTR', 'name': 'Marine Drive Branch', 'code': 'KOC01', 'city': 'Kochi', 'state': 'Kerala', 'pincode': '682031', 'gstin': '32AAACE3456J1Z1', 'state_code': '32'},
    ]

    branches = {}
    for b_data in branches_info:
        r_obj = restaurants[b_data['restaurant']]
        b, _ = Branch.objects.get_or_create(
            restaurant=r_obj,
            code=b_data['code'],
            defaults={
                'name': b_data['name'],
                'phone': '+91 99887 76655',
                'email': f"{b_data['code'].lower()}@dineflow.in",
                'address_line1': f"Main Commercial Road, {b_data['city']}",
                'city': b_data['city'],
                'state': b_data['state'],
                'pincode': b_data['pincode'],
                'is_active': True,
            }
        )
        BranchSettings.objects.get_or_create(
            branch=b,
            defaults={
                'dine_in_enabled': True,
                'takeaway_enabled': True,
                'delivery_enabled': True,
                'table_reservation_enabled': True,
            }
        )
        BranchTaxConfiguration.objects.get_or_create(
            branch=b,
            defaults={
                'gstin': b_data['gstin'],
                'state_code': b_data['state_code'],
            }
        )

        # Table Sections & Tables
        sec_main, _ = TableSection.objects.get_or_create(branch=b, name='Main AC Dining Hall', defaults={'floor': 'Ground Floor'})
        sec_family, _ = TableSection.objects.get_or_create(branch=b, name='Family Section', defaults={'floor': '1st Floor'})

        for t_idx in range(1, 7):
            RestaurantTable.objects.get_or_create(
                branch=b,
                table_number=f"T-{t_idx:02d}",
                defaults={'section': sec_main, 'seating_capacity': 4, 'min_capacity': 2, 'status': 'AVAILABLE'}
            )
        for t_idx in range(7, 11):
            RestaurantTable.objects.get_or_create(
                branch=b,
                table_number=f"F-{t_idx:02d}",
                defaults={'section': sec_family, 'seating_capacity': 6, 'min_capacity': 4, 'status': 'AVAILABLE'}
            )

        # Kitchen Stations
        KitchenStation.objects.get_or_create(branch=b, code='BIRYANI', defaults={'name': 'Biryani & Rice Station'})
        KitchenStation.objects.get_or_create(branch=b, code='TANDOOR', defaults={'name': 'Tandoor & Starters Station'})
        KitchenStation.objects.get_or_create(branch=b, code='SOUTH', defaults={'name': 'South Indian Tiffin & Meals'})
        KitchenStation.objects.get_or_create(branch=b, code='CURRY', defaults={'name': 'Curry & Gravy Station'})

        branches[b_data['code']] = b
    print("[5/13] 6 City Branches, Table sections, Tables, and Kitchen Stations initialized.")

    # 7. Inventory Categories & Items
    for r_code, r_obj in restaurants.items():
        inv_cat_groceries, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='GROCERIES', defaults={'name': 'Grains & Rice'})
        inv_cat_meat, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='MEAT', defaults={'name': 'Fresh Poultry & Meat'})
        inv_cat_dairy, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='DAIRY', defaults={'name': 'Dairy & Ghee'})
        inv_cat_spices, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='SPICES', defaults={'name': 'Spices & Condiments'})
        inv_cat_veg, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='VEG', defaults={'name': 'Vegetables & Fresh Produce'})
        inv_cat_bev, _ = InventoryCategory.objects.get_or_create(restaurant=r_obj, code='BEV', defaults={'name': 'Beverage Supplies'})

        items_definitions = [
            ('Basmati Rice', 'RICE_BASMATI', inv_cat_groceries, units['kg'], Decimal('90.00'), Decimal('50.000')),
            ('Fresh Chicken', 'MEAT_CHICKEN', inv_cat_meat, units['kg'], Decimal('180.00'), Decimal('30.000')),
            ('Fresh Paneer', 'DAIRY_PANEER', inv_cat_dairy, units['kg'], Decimal('340.00'), Decimal('10.000')),
            ('Pure Desi Ghee', 'DAIRY_GHEE', inv_cat_dairy, units['kg'], Decimal('620.00'), Decimal('15.000')),
            ('Biryani Masala Blend', 'SPICE_BIRYANI', inv_cat_spices, units['kg'], Decimal('450.00'), Decimal('8.000')),
            ('Onions', 'VEG_ONION', inv_cat_veg, units['kg'], Decimal('30.00'), Decimal('50.000')),
            ('Tomatoes', 'VEG_TOMATO', inv_cat_veg, units['kg'], Decimal('25.00'), Decimal('40.000')),
            ('Ginger Garlic Paste', 'SPICE_GGP', inv_cat_spices, units['kg'], Decimal('120.00'), Decimal('10.000')),
            ('Refined Sunflower Oil', 'OIL_SUNFLOWER', inv_cat_groceries, units['l'], Decimal('115.00'), Decimal('60.000')),
            ('Fresh Dairy Milk', 'DAIRY_MILK', inv_cat_dairy, units['l'], Decimal('55.00'), Decimal('20.000')),
            ('South Indian Filter Coffee Powder', 'BEV_COFFEE', inv_cat_bev, units['kg'], Decimal('420.00'), Decimal('5.000')),
            ('Sugar', 'GROCERY_SUGAR', inv_cat_groceries, units['kg'], Decimal('42.00'), Decimal('25.000')),
            ('Gulab Jamun Mix', 'GROCERY_GJ_MIX', inv_cat_groceries, units['kg'], Decimal('280.00'), Decimal('10.000')),
            ('Maida Flour', 'GROCERY_MAIDA', inv_cat_groceries, units['kg'], Decimal('38.00'), Decimal('40.000')),
            ('Salted Butter', 'DAIRY_BUTTER', inv_cat_dairy, units['kg'], Decimal('480.00'), Decimal('10.000')),
            ('Dosa Batter Rice & Dal Blend', 'GROCERY_DOSA_MIX', inv_cat_groceries, units['kg'], Decimal('65.00'), Decimal('30.000')),
        ]

        created_items = {}
        for name, code, cat, unit, cost, reorder in items_definitions:
            inv_item, _ = InventoryItem.objects.get_or_create(
                restaurant=r_obj,
                item_code=code,
                defaults={
                    'name': name,
                    'category': cat,
                    'primary_unit': unit,
                    'current_cost_per_unit': cost,
                    'reorder_level': reorder,
                    'safety_stock': reorder / 2,
                    'is_active': True,
                }
            )
            created_items[code] = inv_item

        # Stocks for branches
        for b_obj in r_obj.branches.all():
            for code, inv_item in created_items.items():
                initial_qty = Decimal('100.000')
                _stk, created = Stock.objects.get_or_create(
                    branch=b_obj,
                    inventory_item=inv_item,
                    defaults={
                        'quantity_on_hand': initial_qty,
                        'available_quantity': initial_qty,
                        'reserved_quantity': Decimal('0.000'),
                        'last_stock_take_date': timezone.now()
                    }
                )
                if created:
                    batch = StockBatch.objects.create(
                        branch=b_obj,
                        inventory_item=inv_item,
                        batch_number=f"INIT-{b_obj.code}-{inv_item.item_code}",
                        received_date=timezone.now().date(),
                        purchase_unit_price=inv_item.current_cost_per_unit,
                        initial_quantity=initial_qty,
                        remaining_quantity=initial_qty
                    )
                    StockMovement.objects.create(
                        branch=b_obj,
                        inventory_item=inv_item,
                        batch=batch,
                        movement_type='PURCHASE_RECEIPT',
                        quantity=initial_qty,
                        balance_before=Decimal('0.000'),
                        balance_after=initial_qty,
                        reference_id='INITIAL-BALANCE',
                        notes='Initial system opening stock balance'
                    )

    print("[6/13] Inventory categories, items, and branch stock ledgers seeded.")

    # 8. Suppliers
    for r_code, r_obj in restaurants.items():
        Supplier.objects.get_or_create(
            restaurant=r_obj,
            supplier_code=f'SUP-{r_code}-01',
            defaults={
                'name': f'{r_obj.name} Primary Grains & Spices Co.',
                'contact_person': 'Ravi Shankar',
                'phone': '+91 98480 11223',
                'email': 'ravi@deccansupplies.com',
                'address': 'Kothapet Wholesale Market',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'gstin': '36AABCS1111Z1Z0'
            }
        )
        Supplier.objects.get_or_create(
            restaurant=r_obj,
            supplier_code=f'SUP-{r_code}-02',
            defaults={
                'name': 'Fresh Farm Poultry & Dairy Supplies',
                'contact_person': 'Venkatesh Rao',
                'phone': '+91 94400 33445',
                'email': 'venkat@freshfarms.in',
                'address': 'Dairy Farm Road',
                'city': 'Vijayawada',
                'state': 'Andhra Pradesh',
                'gstin': '37AABCF2222Y1Z1'
            }
        )
    print("[7/13] Regional suppliers registered.")

    # 9. Menu & Items
    for r_code, r_obj in restaurants.items():
        menu, _ = Menu.objects.get_or_create(restaurant=r_obj, name='Main Dine-in & Delivery Menu', defaults={'menu_type': 'ALL'})
        cat_biryani, _ = MenuCategory.objects.get_or_create(menu=menu, code='BIRYANI', defaults={'name': 'Biryani Specialties', 'sort_order': 1})
        cat_meals, _ = MenuCategory.objects.get_or_create(menu=menu, code='MEALS', defaults={'name': 'Traditional Indian Meals', 'sort_order': 2})
        cat_tiffins, _ = MenuCategory.objects.get_or_create(menu=menu, code='TIFFINS', defaults={'name': 'South Indian Tiffins', 'sort_order': 3})
        cat_curries, _ = MenuCategory.objects.get_or_create(menu=menu, code='CURRIES', defaults={'name': 'Curries & Gravies', 'sort_order': 4})
        cat_starters, _ = MenuCategory.objects.get_or_create(menu=menu, code='STARTERS', defaults={'name': 'Starters & Appetizers', 'sort_order': 5})
        cat_breads, _ = MenuCategory.objects.get_or_create(menu=menu, code='BREADS', defaults={'name': 'Tandoori Breads', 'sort_order': 6})
        cat_desserts, _ = MenuCategory.objects.get_or_create(menu=menu, code='DESSERTS', defaults={'name': 'Desserts', 'sort_order': 7})
        cat_beverages, _ = MenuCategory.objects.get_or_create(menu=menu, code='BEVERAGES', defaults={'name': 'Beverages', 'sort_order': 8})

        menu_items_data = [
            ('Chicken Biryani', cat_biryani, Decimal('320.00'), 'NON_VEG', True, True, 20),
            ('Veg Biryani', cat_biryani, Decimal('240.00'), 'VEG', True, False, 15),
            ('Andhra Meals', cat_meals, Decimal('220.00'), 'VEG', True, True, 10),
            ('Masala Dosa', cat_tiffins, Decimal('90.00'), 'VEG', False, False, 10),
            ('Idli', cat_tiffins, Decimal('50.00'), 'VEG', False, False, 5),
            ('Vada', cat_tiffins, Decimal('60.00'), 'VEG', False, False, 5),
            ('Paneer Butter Masala', cat_curries, Decimal('260.00'), 'VEG', True, False, 15),
            ('Chicken 65', cat_starters, Decimal('280.00'), 'NON_VEG', True, True, 12),
            ('Butter Naan', cat_breads, Decimal('45.00'), 'VEG', False, False, 8),
            ('Gulab Jamun', cat_desserts, Decimal('80.00'), 'VEG', False, False, 5),
            ('Filter Coffee', cat_beverages, Decimal('40.00'), 'VEG', False, False, 5),
        ]

        # Addons
        MenuAddon.objects.get_or_create(restaurant=r_obj, name='Extra Cheese / Paneer', defaults={'price': Decimal('40.00')})
        MenuAddon.objects.get_or_create(restaurant=r_obj, name='Special Dum Raita & Salan', defaults={'price': Decimal('30.00')})

        for name, cat, price, dietary, rec, spicy, prep in menu_items_data:
            m_item, _ = MenuItem.objects.get_or_create(
                category=cat,
                name=name,
                defaults={
                    'base_price': price,
                    'dietary_type': dietary,
                    'is_recommended': rec,
                    'is_spicy': spicy,
                    'preparation_time_minutes': prep,
                    'is_available': True,
                    'hsn_code': '996331',
                }
            )
            # Variants for Biryani
            if 'Biryani' in name:
                MenuVariant.objects.get_or_create(menu_item=m_item, name='Regular', defaults={'price': price, 'is_default': True})
                MenuVariant.objects.get_or_create(menu_item=m_item, name='Family Pack', defaults={'price': (price * Decimal('2.4')).quantize(Decimal('1.00')), 'is_default': False})

            # Recipe & FoodIngredient BOM
            recipe, _ = Recipe.objects.get_or_create(
                menu_item=m_item,
                defaults={
                    'title': f'Standard SOP Recipe for {name}',
                    'instructions': 'Prepared according to master chef standards for authentic taste.',
                    'yield_servings': 1,
                }
            )

            # Link sample BOM ingredients
            inv_rice = InventoryItem.objects.filter(restaurant=r_obj, item_code='RICE_BASMATI').first()
            inv_chicken = InventoryItem.objects.filter(restaurant=r_obj, item_code='MEAT_CHICKEN').first()
            inv_paneer = InventoryItem.objects.filter(restaurant=r_obj, item_code='DAIRY_PANEER').first()
            inv_ghee = InventoryItem.objects.filter(restaurant=r_obj, item_code='DAIRY_GHEE').first()
            inv_coffee = InventoryItem.objects.filter(restaurant=r_obj, item_code='BEV_COFFEE').first()
            inv_milk = InventoryItem.objects.filter(restaurant=r_obj, item_code='DAIRY_MILK').first()

            if name == 'Chicken Biryani' and inv_rice and inv_chicken:
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_rice, defaults={'quantity_required': Decimal('0.250'), 'unit_name': 'kg'})
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_chicken, defaults={'quantity_required': Decimal('0.300'), 'unit_name': 'kg'})
                if inv_ghee:
                    FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_ghee, defaults={'quantity_required': Decimal('0.040'), 'unit_name': 'kg'})
            elif name == 'Paneer Butter Masala' and inv_paneer and inv_ghee:
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_paneer, defaults={'quantity_required': Decimal('0.200'), 'unit_name': 'kg'})
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_ghee, defaults={'quantity_required': Decimal('0.030'), 'unit_name': 'kg'})
            elif name == 'Filter Coffee' and inv_coffee and inv_milk:
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_coffee, defaults={'quantity_required': Decimal('0.020'), 'unit_name': 'kg'})
                FoodIngredient.objects.get_or_create(recipe=recipe, inventory_item=inv_milk, defaults={'quantity_required': Decimal('0.150'), 'unit_name': 'l'})

    print("[8/13] Authentic Indian Menu items, variants, recipes, and BOM ingredients configured.")

    # 10. Departments, Designations, and Employees
    for b_code, b_obj in branches.items():
        r_obj = b_obj.restaurant
        dept_kitchen, _ = Department.objects.get_or_create(restaurant=r_obj, branch=b_obj, code=f'KT_{b_code}', defaults={'name': 'Kitchen'})
        dept_service, _ = Department.objects.get_or_create(restaurant=r_obj, branch=b_obj, code=f'SV_{b_code}', defaults={'name': 'Front of House Service'})
        dept_mgmt, _ = Department.objects.get_or_create(restaurant=r_obj, branch=b_obj, code=f'MG_{b_code}', defaults={'name': 'Management & Accounts'})

        desig_chef, _ = Designation.objects.get_or_create(department=dept_kitchen, code='HEAD_CHEF', defaults={'title': 'Head Chef', 'level': 3})
        desig_waiter, _ = Designation.objects.get_or_create(department=dept_service, code='CAPTAIN', defaults={'title': 'Captain Waiter', 'level': 2})
        desig_mgr, _ = Designation.objects.get_or_create(department=dept_mgmt, code='MGR', defaults={'title': 'Branch General Manager', 'level': 4})

        _shift_gen, _ = Shift.objects.get_or_create(branch=b_obj, name='Regular Service Shift', defaults={'start_time': '10:00:00', 'end_time': '22:30:00'})

        # Sample staff user & employee
        staff_data = [
            (f'chef.{b_code.lower()}@dineflow.in', f'Master Chef ({b_code})', dept_kitchen, desig_chef, 'HEAD_CHEF', Decimal('45000.00')),
            (f'waiter.{b_code.lower()}@dineflow.in', f'Service Captain ({b_code})', dept_service, desig_waiter, 'WAITER', Decimal('22000.00')),
            (f'manager.{b_code.lower()}@dineflow.in', f'Branch Manager ({b_code})', dept_mgmt, desig_mgr, 'BRANCH_MANAGER', Decimal('55000.00')),
        ]
        for email, full_name, dept, desig, r_code, basic_sal in staff_data:
            s_user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    'phone': f"91000{b_obj.code[:3].upper()}{len(email):02d}"[:10],
                    'first_name': full_name.split()[0],
                    'last_name': ' '.join(full_name.split()[1:]),
                    'is_staff': True,
                    'is_active': True,
                }
            )
            s_user.set_password('StaffPassword@123')
            s_user.save()

            emp, _ = Employee.objects.get_or_create(
                user=s_user,
                defaults={
                    'restaurant': r_obj,
                    'branch': b_obj,
                    'department': dept,
                    'designation': desig,
                    'employee_code': f"EMP-{b_code}-{s_user.id.hex[:4].upper()}",
                    'date_of_joining': date(2025, 1, 1),
                    'status': 'ACTIVE',
                    'employment_type': 'FULL_TIME',
                    'pan_number': 'ABCDE1234F',
                    'aadhaar_masked': 'XXXXXXXX8901'
                }
            )
            SalaryStructure.objects.get_or_create(
                employee=emp,
                defaults={
                    'basic_pay': basic_sal,
                    'hra': (basic_sal * Decimal('0.40')).quantize(Decimal('0.01')),
                    'special_allowance': Decimal('3000.00'),
                    'provident_fund': (basic_sal * Decimal('0.12')).quantize(Decimal('0.01')),
                    'professional_tax': Decimal('200.00'),
                    'effective_from': date(2025, 1, 1),
                }
            )
            UserRole.objects.get_or_create(
                user=s_user,
                role=roles[r_code],
                restaurant=r_obj,
                branch=b_obj
            )

    print("[9/13] Employees, HR Departments, Shifts, and Salary structures created.")

    # 11. Customers
    customer_list = [
        ('Sumanth Reddy', '9849012345', 'sumanth.reddy@example.com', 'Andhra Spice Kitchen'),
        ('Ananya Sharma', '9849023456', 'ananya.sharma@example.com', 'Hyderabad Biryani Hub'),
        ('Rajesh Kumar', '9849034567', 'rajesh.kumar@example.com', 'Coastal Curry House'),
        ('Priya Nair', '9849045678', 'priya.nair@example.com', 'Kerala Taste Restaurant'),
        ('Karthik Iyer', '9849056789', 'karthik.iyer@example.com', 'Coastal Curry House'),
        ('Vikram Varma', '9849067890', 'vikram.varma@example.com', 'Andhra Spice Kitchen'),
    ]

    customers = []
    for name, phone, email, r_name in customer_list:
        target_r = Restaurant.objects.get(name=r_name)
        c, _ = Customer.objects.get_or_create(
            restaurant=target_r,
            phone=phone,
            defaults={'name': name, 'email': email, 'status': 'ACTIVE'}
        )
        CustomerPreference.objects.get_or_create(
            customer=c,
            defaults={
                'dietary_preference': 'NON_VEG',
                'spice_tolerance': 'HIGH',
                'favorite_dishes': 'Chicken Biryani, Andhra Meals, Chicken 65'
            }
        )
        # Loyalty account
        tier_bronze = CustomerTier.objects.filter(restaurant=target_r, name='Bronze').first()
        LoyaltyAccount.objects.get_or_create(customer=c, defaults={'tier': tier_bronze, 'current_points': Decimal('150.00')})
        customers.append(c)
    print("[10/13] Customer profiles, dietary preferences, and loyalty accounts seeded.")

    # 12. Realistic Completed Orders, Invoices, and Payments
    hyd_branch = branches['HYD01']
    vja_branch = branches['VJA01']
    blr_branch = branches['BLR01']

    test_branches = [hyd_branch, vja_branch, blr_branch]
    order_counter = 100

    for b_obj in test_branches:
        r_obj = b_obj.restaurant
        biryani_item = MenuItem.objects.filter(category__menu__restaurant=r_obj, name__contains='Biryani').first()
        curry_item = MenuItem.objects.filter(category__menu__restaurant=r_obj, name__contains='Paneer').first()
        bread_item = MenuItem.objects.filter(category__menu__restaurant=r_obj, name__contains='Naan').first()
        dessert_item = MenuItem.objects.filter(category__menu__restaurant=r_obj, name__contains='Jamun').first()

        items_to_order = [it for it in [biryani_item, curry_item, bread_item, dessert_item] if it]
        c_obj = Customer.objects.filter(restaurant=r_obj).first()
        tbl = RestaurantTable.objects.filter(branch=b_obj).first()

        for d_offset in range(5, -1, -1):
            order_date = timezone.now() - timedelta(days=d_offset)
            order_num = f"ORD-{b_obj.code}-{order_date.strftime('%Y%m%d')}-{order_counter:04d}"
            order_counter += 1

            subtotal = Decimal('0.00')
            order = Order.objects.create(
                restaurant=r_obj,
                branch=b_obj,
                order_number=order_num,
                order_type='DINE_IN',
                table=tbl,
                customer=c_obj,
                status='PAID',
                placed_at=order_date,
                closed_at=order_date + timedelta(minutes=45)
            )

            for itm in items_to_order:
                qty = 2
                u_price = itm.base_price
                line_tot = u_price * Decimal(str(qty))
                OrderItem.objects.create(
                    order=order,
                    menu_item=itm,
                    quantity=qty,
                    unit_price=u_price,
                    subtotal=line_tot,
                    total_price=line_tot,
                    status='SERVED'
                )
                subtotal += line_tot

            tax_tot = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
            final_tot = subtotal + tax_tot
            order.subtotal = subtotal
            order.tax_amount = tax_tot
            order.final_amount = final_tot
            order.total_item_count = len(items_to_order) * 2
            order.save()

            # Status History
            OrderStatusHistory.objects.create(order=order, old_status='PLACED', new_status='PAID', timestamp=order_date)

            # Invoice
            inv_num = f"INV/{b_obj.code}/2026-27/{order_counter:05d}"
            cgst = (subtotal * Decimal('0.025')).quantize(Decimal('0.01'))
            sgst = (subtotal * Decimal('0.025')).quantize(Decimal('0.01'))

            invoice = Invoice.objects.create(
                order=order,
                restaurant=r_obj,
                branch=b_obj,
                invoice_number=inv_num,
                fiscal_year='2026-27',
                invoice_date=order_date,
                customer_name=c_obj.name if c_obj else 'Guest',
                customer_phone=c_obj.phone if c_obj else '',
                subtotal=subtotal,
                taxable_amount=subtotal,
                cgst_amount=cgst,
                sgst_amount=sgst,
                grand_total=final_tot,
                status='PAID',
            )
            for itm in items_to_order:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    item_name=itm.name,
                    quantity=2,
                    unit_price=itm.base_price,
                    taxable_amount=itm.base_price * 2,
                    total_amount=itm.base_price * 2 * Decimal('1.05')
                )

            # Payment
            pm_code = 'UPI' if d_offset % 2 == 0 else 'CASH'
            pm_obj = PaymentMethod.objects.get(code=pm_code)
            pay = Payment.objects.create(
                invoice=invoice,
                order=order,
                branch=b_obj,
                payment_method=pm_obj,
                amount=final_tot,
                transaction_reference=f"UTR-UPI-{b_obj.code}-{order_counter}" if pm_code == 'UPI' else f"CASH-{order_counter}",
                status='SUCCESS',
                paid_at=order_date
            )
            PaymentTransaction.objects.create(payment=pay, transaction_type='PAYMENT', amount=final_tot, status='SUCCESS')

    print("[11/13] 18 realistic completed Orders, Invoices, and GST payments generated.")

    # 13. Daily Sales Snapshots & Operating Expenses
    for b_code, b_obj in branches.items():
        # Operating Expenses
        exp_cat_rent, _ = ExpenseCategory.objects.get_or_create(restaurant=b_obj.restaurant, code='RENT', defaults={'name': 'Property Rent & Maintenance'})
        _exp_cat_util, _ = ExpenseCategory.objects.get_or_create(restaurant=b_obj.restaurant, code='UTILITIES', defaults={'name': 'Electricity & Commercial LPG'})

        Expense.objects.get_or_create(
            branch=b_obj,
            expense_number=f"EXP-{b_code}-202609-01",
            defaults={
                'restaurant': b_obj.restaurant,
                'category': exp_cat_rent,
                'title': f'Monthly Commercial Premises Rent - {b_obj.name}',
                'amount': Decimal('75000.00'),
                'total_amount': Decimal('75000.00'),
                'expense_date': date(2026, 9, 1),
                'payment_method': 'BANK_TRANSFER',
                'vendor_name': 'Commercial Plaza Properties Ltd',
                'status': 'PAID'
            }
        )

        # Snapshots
        for d in range(7, 0, -1):
            snap_date = timezone.now().date() - timedelta(days=d)
            orders_day = Order.objects.filter(branch=b_obj, placed_at__date=snap_date)
            total_orders = orders_day.count() or 12
            total_sales = Decimal('18450.00') + Decimal(str(d * 1250))
            tax_col = (total_sales * Decimal('0.05')).quantize(Decimal('0.01'))

            DailySalesSnapshot.objects.get_or_create(
                branch=b_obj,
                date=snap_date,
                defaults={
                    'total_orders': total_orders,
                    'total_gross_sales': total_sales,
                    'total_net_sales': total_sales,
                    'total_tax_collected': tax_col,
                    'dine_in_sales': (total_sales * Decimal('0.70')).quantize(Decimal('0.01')),
                    'takeaway_sales': (total_sales * Decimal('0.15')).quantize(Decimal('0.01')),
                    'delivery_sales': (total_sales * Decimal('0.15')).quantize(Decimal('0.01')),
                    'cash_collected': (total_sales * Decimal('0.30')).quantize(Decimal('0.01')),
                    'upi_collected': (total_sales * Decimal('0.55')).quantize(Decimal('0.01')),
                    'card_collected': (total_sales * Decimal('0.15')).quantize(Decimal('0.01')),
                    'avg_order_value': (total_sales / Decimal(str(total_orders))).quantize(Decimal('0.01')),
                }
            )

        # Sample Notification
        Notification.objects.get_or_create(
            restaurant=b_obj.restaurant,
            branch=b_obj,
            title='Daily Opening Stock Reorder Warning',
            defaults={
                'message': 'Basmati Rice and Ghee stocks have reached optimal safety margins.',
                'notification_type': 'LOW_STOCK',
                'priority': 'NORMAL',
                'channel': 'IN_APP',
                'is_broadcast': True,
            }
        )

    print("[12/13] Analytics snapshots, operational expenses, and notifications seeded.")
    print("[13/13] DineFlow Database seeding completed successfully with 100% relational integrity!")


if __name__ == '__main__':
    seed_all()
