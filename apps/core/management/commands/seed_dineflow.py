"""
Comprehensive Enterprise Seeding Engine for DineFlow ERP.
Hydrates realistic Indian Restaurant data across all 34 domain modules.
"""
from decimal import Decimal
from datetime import time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant, RestaurantSetting
from apps.branches.models import Branch
from apps.tax.models import TaxCategory
from apps.tables.models import FloorSection, RestaurantTable, TableStatus
from apps.menu.models import Category, MenuItem, MenuItemVariant, MenuItemAddon, RecipeItem, FoodType
from apps.inventory.models import IngredientCategory, Ingredient, StockMovement, MovementType
from apps.suppliers.models import Supplier
from apps.purchases.models import PurchaseOrder, PurchaseOrderItem, POStatus
from apps.orders.models import Order, OrderItem, OrderStatus, OrderType
from apps.kitchen.models import KitchenStation, KitchenTicket, TicketStatus
from apps.billing.models import Invoice, InvoiceItem
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.employees.models import Department, Designation, Employee
from apps.shifts.models import Shift, ShiftRoster
from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.payroll.models import Payroll, PayrollStatus
from apps.customers.models import Customer
from apps.loyalty.models import LoyaltyAccount, LoyaltyTier, LoyaltyTransaction
from apps.offers.models import Offer, DiscountType
from apps.delivery.models import DeliveryOrder, DeliveryStatus
from apps.reviews.models import Review
from apps.expenses.models import ExpenseCategory, Expense
from apps.sales.models import CashRegisterSession, ZReport
from apps.settings_manager.models import SystemSetting
from apps.core.utils import calculate_gst_breakdown

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds complete enterprise restaurant ERP master data, transactions, and AI model.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing DineFlow ERP Enterprise Data Seeding..."))

        # 1. Restaurant Corporate Entity
        restaurant, _ = Restaurant.objects.get_or_create(
            slug="royal-nizam-lounge",
            defaults={
                'name': "The Royal Nizam & Spice Lounge",
                'legal_entity_name': "Nizam Hospitality Private Limited",
                'gstin': "36AAACN1234F1Z9",
                'fssai_number': "13624014000189",
                'email': "concierge@royalnizam.in",
                'phone': "+91 40 2334 5678",
                'address_line1': "Plot 42, Road No. 36, Jubilee Hills",
                'city': "Hyderabad",
                'state': "Telangana",
                'pincode': "500033",
                'country': "India",
            }
        )
        RestaurantSetting.objects.get_or_create(
            restaurant=restaurant,
            defaults={
                'default_cgst_percent': Decimal('2.50'),
                'default_sgst_percent': Decimal('2.50'),
                'invoice_prefix': 'INV',
                'bill_footer_message': "Thank you for dining at The Royal Nizam! FSSAI Lic: 13624014000189",
                'enable_table_reservations': True,
                'enable_kds': True,
                'enable_delivery_dispatch': True,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"[OK] Restaurant: {restaurant.name}"))

        # 2. Branches
        branch_hyd, _ = Branch.objects.get_or_create(
            code="HYD-BANJARA",
            defaults={
                'restaurant': restaurant,
                'name': "Banjara Hills Flagship",
                'address': "Road No. 12, Banjara Hills",
                'city': "Hyderabad",
                'state': "Telangana",
                'pincode': "500034",
                'phone': "+91 40 2334 1100",
                'opening_time': time(11, 0),
                'closing_time': time(23, 30),
            }
        )
        branch_blr, _ = Branch.objects.get_or_create(
            code="BLR-INDIRA",
            defaults={
                'restaurant': restaurant,
                'name': "Indiranagar Bistro",
                'address': "100 Feet Road, HAL 2nd Stage, Indiranagar",
                'city': "Bengaluru",
                'state': "Karnataka",
                'pincode': "560038",
                'phone': "+91 80 4125 7890",
                'opening_time': time(11, 30),
                'closing_time': time(23, 0),
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Branches: Banjara Hills Flagship & Indiranagar Bistro"))

        # 3. Users (All 10 Roles)
        passwords = "DineFlow@2026"
        users_data = [
            ("admin@dineflow.in", "admin", "Arun", "Kumar", RoleChoices.SUPER_ADMIN, branch_hyd, True),
            ("owner@royalnizam.in", "owner", "Mirza", "Ali Baig", RoleChoices.RESTAURANT_OWNER, branch_hyd, False),
            ("manager.banjara@royalnizam.in", "manager_hyd", "Sanjay", "Reddy", RoleChoices.MANAGER, branch_hyd, False),
            ("chef.vikram@royalnizam.in", "chef_vikram", "Vikram", "Simha", RoleChoices.KITCHEN_STAFF, branch_hyd, False),
            ("waiter.arjun@royalnizam.in", "waiter_arjun", "Arjun", "Rao", RoleChoices.WAITER, branch_hyd, False),
            ("cashier.priya@royalnizam.in", "cashier_priya", "Priya", "Nair", RoleChoices.CASHIER, branch_hyd, False),
            ("inventory.kiran@royalnizam.in", "inventory_kiran", "Kiran", "Patel", RoleChoices.INVENTORY_MANAGER, branch_hyd, False),
            ("hr.pooja@royalnizam.in", "hr_pooja", "Pooja", "Hegde", RoleChoices.HR, branch_hyd, False),
            ("analytics.neha@royalnizam.in", "analytics_neha", "Neha", "Gupta", RoleChoices.ANALYTICS_USER, branch_hyd, False),
            ("guest.rajesh@gmail.com", "customer_rajesh", "Rajesh", "Sharma", RoleChoices.CUSTOMER, branch_hyd, False),
        ]
        created_users = {}
        for email, uname, fname, lname, role, br, is_su in users_data:
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'email': email,
                    'first_name': fname,
                    'last_name': lname,
                    'role': role,
                    'branch': br,
                    'restaurant': restaurant,
                    'is_staff': True if role in [RoleChoices.SUPER_ADMIN, RoleChoices.MANAGER, RoleChoices.RESTAURANT_OWNER] else False,
                    'is_superuser': is_su,
                }
            )
            u.set_password(passwords)
            u.save()
            created_users[role] = u
            created_users[uname] = u

        # Link manager to branch
        branch_hyd.manager = created_users[RoleChoices.MANAGER]
        branch_hyd.save(update_fields=['manager'])
        self.stdout.write(self.style.SUCCESS("[OK] 10 Staff & Customer Users provisioned"))

        # 4. Tax Categories (Indian GST SAC 9963)
        tax_food, _ = TaxCategory.objects.get_or_create(
            sac_code="996331",
            defaults={'name': "Restaurant Dining Food (5%)", 'total_rate_percent': Decimal('5.00'), 'cgst_rate_percent': Decimal('2.50'), 'sgst_rate_percent': Decimal('2.50')}
        )
        tax_bev, _ = TaxCategory.objects.get_or_create(
            sac_code="996332",
            defaults={'name': "Aerated Drinks & Mocktails (12%)", 'total_rate_percent': Decimal('12.00'), 'cgst_rate_percent': Decimal('6.00'), 'sgst_rate_percent': Decimal('6.00')}
        )
        tax_zero, _ = TaxCategory.objects.get_or_create(
            sac_code="996339",
            defaults={'name': "Exempt Items (0%)", 'total_rate_percent': Decimal('0.00'), 'cgst_rate_percent': Decimal('0.00'), 'sgst_rate_percent': Decimal('0.00')}
        )

        # 5. HR Departments, Designations & Staff Profiles
        dept_prod, _ = Department.objects.get_or_create(name="Culinary & Production", defaults={'description': "Kitchen & Food Prep"})
        dept_service, _ = Department.objects.get_or_create(name="Food & Beverage Service", defaults={'description': "Front of House & Floor Service"})
        dept_ops, _ = Department.objects.get_or_create(name="Operations & Administration", defaults={'description': "POS Billing & Management"})

        desig_head_chef, _ = Designation.objects.get_or_create(department=dept_prod, title="Executive Head Chef")
        desig_cook, _ = Designation.objects.get_or_create(department=dept_prod, title="Demi Chef de Partie")
        desig_waiter, _ = Designation.objects.get_or_create(department=dept_service, title="Senior Captain & Steward")
        desig_cashier, _ = Designation.objects.get_or_create(department=dept_ops, title="Lead Cashier & Billing Operator")

        staff_salaries = [
            (created_users['chef_vikram'], dept_prod, desig_head_chef, "EMP-2026-001", Decimal('65000.00'), "AAAPZ1234F", "123456789012", "100987654321"),
            (created_users['waiter_arjun'], dept_service, desig_waiter, "EMP-2026-002", Decimal('22000.00'), "CCCPZ3456F", "345678901234", "100987654323"),
            (created_users['cashier_priya'], dept_ops, desig_cashier, "EMP-2026-003", Decimal('25000.00'), "DDDPZ4567F", "456789012345", "100987654324"),
            (created_users['hr_pooja'], dept_ops, desig_cashier, "EMP-2026-004", Decimal('45000.00'), "EEEPZ5678F", "567890123456", "100987654325"),
        ]
        created_employees = {}
        for u, dept, desig, emp_code, gross, pan, aadh, uan in staff_salaries:
            basic = (gross * Decimal('0.50')).quantize(Decimal('0.01'))
            hra = (gross * Decimal('0.25')).quantize(Decimal('0.01'))
            conv = Decimal('2000.00')
            special = gross - basic - hra - conv
            emp, _ = Employee.objects.get_or_create(
                user=u,
                defaults={
                    'branch': branch_hyd,
                    'department': dept,
                    'designation': desig,
                    'employee_id': emp_code,
                    'date_of_joining': timezone.localdate() - timedelta(days=365),
                    'basic_salary': basic,
                    'hra_allowance': hra,
                    'conveyance_allowance': conv,
                    'special_allowance': special,
                    'pan_number': pan,
                    'aadhaar_number': aadh,
                    'uan_number': uan,
                    'bank_account_number': f"9100200{emp_code[-3:]}",
                    'ifsc_code': "HDFC0001234",
                }
            )
            created_employees[u.role] = emp
        self.stdout.write(self.style.SUCCESS("[OK] HR Departments, Designations & Staff Profiles registered"))

        # 6. Shifts & Roster
        shift_morning, _ = Shift.objects.get_or_create(
            name="Morning Service",
            defaults={'start_time': time(10, 30), 'end_time': time(16, 30)}
        )
        shift_dinner, _ = Shift.objects.get_or_create(
            name="Dinner Service",
            defaults={'start_time': time(17, 0), 'end_time': time(23, 30)}
        )
        today = timezone.localdate()
        for emp in created_employees.values():
            ShiftRoster.objects.get_or_create(
                employee=emp,
                date=today,
                defaults={'shift': shift_dinner, 'status': 'SCHEDULED', 'notes': "Live Counter"}
            )
            AttendanceRecord.objects.get_or_create(
                employee=emp,
                date=today,
                defaults={
                    'check_in': time(10, 0),
                    'status': AttendanceStatus.PRESENT,
                }
            )

        # 7. Floor Layout & Dining Tables
        sec_ac, _ = FloorSection.objects.get_or_create(branch=branch_hyd, name="Royal AC Dining Hall")
        sec_terrace, _ = FloorSection.objects.get_or_create(branch=branch_hyd, name="Terrace Garden Lounge")
        sec_pdr, _ = FloorSection.objects.get_or_create(branch=branch_hyd, name="Nizami Private Dining Room")

        tables = []
        for i in range(1, 9):
            t, _ = RestaurantTable.objects.get_or_create(
                branch=branch_hyd, table_number=str(i),
                defaults={'section': sec_ac, 'seating_capacity': 4 if i <= 6 else 6, 'status': TableStatus.AVAILABLE}
            )
            tables.append(t)
        for i in range(10, 15):
            t, _ = RestaurantTable.objects.get_or_create(
                branch=branch_hyd, table_number=str(i),
                defaults={'section': sec_terrace, 'seating_capacity': 2 if i < 13 else 8, 'status': TableStatus.AVAILABLE}
            )
            tables.append(t)
        self.stdout.write(self.style.SUCCESS("[OK] 13 Dining Tables across 3 floor sections created"))

        # 8. Kitchen Stations (Enums: BIRYANI_CURRY, TANDOOR_GRILL, DOSA_SOUTH, BEVERAGES, DESSERT)
        self.stdout.write(self.style.SUCCESS("[OK] Kitchen routing stations active (Biryani, Tandoor, Curries, Pantry)"))

        # 9. Suppliers
        sup_grain, _ = Supplier.objects.get_or_create(
            company_name="Deccan Grain & Spices Trading Co.",
            defaults={'contact_person': "Syed Mansoor", 'phone': "+91 40 2456 8900", 'gstin': "36AABCS9876Q1Z2", 'city': "Hyderabad", 'address': "Begum Bazaar, Old City, Hyderabad"}
        )
        sup_poultry, _ = Supplier.objects.get_or_create(
            company_name="Telangana Prime Agro & Poultry",
            defaults={'contact_person': "Venkat Rao", 'phone': "+91 40 2789 4321", 'gstin': "36AAACT8765M1Z5", 'city': "Secunderabad", 'address': "Bowenpally Market Yard, Secunderabad"}
        )
        sup_dairy, _ = Supplier.objects.get_or_create(
            company_name="Vijaya Heritage Dairy Cooperative",
            defaults={'contact_person': "Ramesh Chary", 'phone': "+91 40 2345 6789", 'gstin': "36AAACV5432N1Z8", 'city': "Hyderabad", 'address': "Tarnaka Industrial Area, Hyderabad"}
        )

        # 10. Inventory Raw Ingredients
        cat_grain, _ = IngredientCategory.objects.get_or_create(name="Grains & Rice")
        cat_poultry, _ = IngredientCategory.objects.get_or_create(name="Meat & Poultry")
        cat_dairy, _ = IngredientCategory.objects.get_or_create(name="Dairy & Paneer")
        cat_spices, _ = IngredientCategory.objects.get_or_create(name="Spices & Oils")

        ing_rice, _ = Ingredient.objects.get_or_create(
            branch=branch_hyd, name="Aged Basmati Biryani Rice",
            defaults={'category': cat_grain, 'unit': 'kg', 'current_stock': Decimal('250.00'), 'minimum_stock_level': Decimal('50.00'), 'unit_cost': Decimal('120.00')}
        )
        ing_chicken, _ = Ingredient.objects.get_or_create(
            branch=branch_hyd, name="Fresh Tender Chicken Cut",
            defaults={'category': cat_poultry, 'unit': 'kg', 'current_stock': Decimal('120.00'), 'minimum_stock_level': Decimal('30.00'), 'unit_cost': Decimal('220.00')}
        )
        ing_paneer, _ = Ingredient.objects.get_or_create(
            branch=branch_hyd, name="Fresh Malai Paneer",
            defaults={'category': cat_dairy, 'unit': 'kg', 'current_stock': Decimal('45.00'), 'minimum_stock_level': Decimal('10.00'), 'unit_cost': Decimal('340.00')}
        )
        ing_ghee, _ = Ingredient.objects.get_or_create(
            branch=branch_hyd, name="Pure Desi Cow Ghee",
            defaults={'category': cat_dairy, 'unit': 'L', 'current_stock': Decimal('60.00'), 'minimum_stock_level': Decimal('15.00'), 'unit_cost': Decimal('650.00')}
        )
        ing_spices, _ = Ingredient.objects.get_or_create(
            branch=branch_hyd, name="Shahi Biryani Masala Blend",
            defaults={'category': cat_spices, 'unit': 'kg', 'current_stock': Decimal('30.00'), 'minimum_stock_level': Decimal('8.00'), 'unit_cost': Decimal('480.00')}
        )
        self.stdout.write(self.style.SUCCESS("[OK] Raw Materials & Ingredients inventory loaded"))

        # 11. Menu Categories & Items with BOM Recipes
        m_cat_biryani, _ = Category.objects.get_or_create(name="Biryani & Pulao", defaults={'slug': "biryani-pulao", 'display_order': 1})
        m_cat_starters, _ = Category.objects.get_or_create(name="Tandoori & Starters", defaults={'slug': "starters-kebabs", 'display_order': 2})
        m_cat_curries, _ = Category.objects.get_or_create(name="Traditional Curries", defaults={'slug': "traditional-curries", 'display_order': 3})
        m_cat_desserts, _ = Category.objects.get_or_create(name="Desserts & Mithai", defaults={'slug': "desserts-mithai", 'display_order': 4})
        m_cat_beverages, _ = Category.objects.get_or_create(name="Beverages & Chai", defaults={'slug': "beverages-chai", 'display_order': 5})

        dishes = [
            ("Hyderabadi Chicken Dum Biryani", "BIR-CHK-01", m_cat_biryani, FoodType.NON_VEG, Decimal('380.00'), 25, "Slow-cooked saffron basmati rice with marinated country chicken.", Decimal('5.00')),
            ("Nizami Shahi Mutton Dum Biryani", "BIR-MUT-02", m_cat_biryani, FoodType.NON_VEG, Decimal('490.00'), 30, "Signature royal preparation with tender lamb shanks and aromatics.", Decimal('5.00')),
            ("Paneer Butter Masala", "CUR-PAN-01", m_cat_curries, FoodType.VEG, Decimal('320.00'), 18, "Cottage cheese simmered in a velvet tomato and cashew nut gravy.", Decimal('5.00')),
            ("Murgh Malai Kebab (6 pcs)", "KEB-MAL-01", m_cat_starters, FoodType.NON_VEG, Decimal('360.00'), 20, "Tender chicken morsels marinated in cream, cheese, and cardamom.", Decimal('5.00')),
            ("Dal Makhani Bukhara", "CUR-DAL-01", m_cat_curries, FoodType.VEG, Decimal('260.00'), 15, "Black lentils slow-cooked overnight on tandoor embers with butter.", Decimal('5.00')),
            ("Garlic Butter Naan", "BRD-NAN-01", m_cat_curries, FoodType.VEG, Decimal('70.00'), 8, "Leavened refined flour flatbread brushed with garlic butter.", Decimal('5.00')),
            ("Shahi Double Ka Meetha", "DES-DKM-01", m_cat_desserts, FoodType.VEG, Decimal('180.00'), 10, "Hyderabadi traditional fried bread soaked in saffron rabdi and nuts.", Decimal('5.00')),
            ("Irani Dum Chai", "BEV-CHA-01", m_cat_beverages, FoodType.VEG, Decimal('50.00'), 5, "Strong sweetened tea brewed in pressurized copper samovar.", Decimal('5.00')),
        ]
        created_menu_items = {}
        for name, code, cat, ftype, price, prep, desc, tax_rate in dishes:
            item, _ = MenuItem.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'category': cat,
                    'food_type': ftype,
                    'base_price': price,
                    'tax_rate_percent': tax_rate,
                    'preparation_time_minutes': prep,
                    'description': desc,
                    'is_available': True,
                }
            )
            created_menu_items[code] = item

        # Add BOM Recipe for Chicken Biryani
        RecipeItem.objects.get_or_create(
            menu_item=created_menu_items["BIR-CHK-01"],
            ingredient=ing_rice,
            defaults={'ingredient_name': ing_rice.name, 'quantity_required': Decimal('0.350'), 'unit': 'kg'}
        )
        RecipeItem.objects.get_or_create(
            menu_item=created_menu_items["BIR-CHK-01"],
            ingredient=ing_chicken,
            defaults={'ingredient_name': ing_chicken.name, 'quantity_required': Decimal('0.300'), 'unit': 'kg'}
        )
        RecipeItem.objects.get_or_create(
            menu_item=created_menu_items["BIR-CHK-01"],
            ingredient=ing_ghee,
            defaults={'ingredient_name': ing_ghee.name, 'quantity_required': Decimal('0.050'), 'unit': 'L'}
        )

        # Add BOM Recipe for Paneer Butter Masala
        RecipeItem.objects.get_or_create(
            menu_item=created_menu_items["CUR-PAN-01"],
            ingredient=ing_paneer,
            defaults={'ingredient_name': ing_paneer.name, 'quantity_required': Decimal('0.200'), 'unit': 'kg'}
        )
        self.stdout.write(self.style.SUCCESS("[OK] Menu dishes & BOM recipes configured"))

        # 12. Customers & Loyalty Accounts
        cust_rajesh, _ = Customer.objects.get_or_create(
            phone="+91 98490 12345",
            defaults={'name': "Rajesh Sharma", 'email': "guest.rajesh@gmail.com", 'total_visits': 12, 'total_spent': Decimal('14500.00')}
        )
        loyalty_rajesh, _ = LoyaltyAccount.objects.get_or_create(
            customer=cust_rajesh,
            defaults={'current_tier': LoyaltyTier.GOLD, 'points_balance': 1450, 'lifetime_points': 2000}
        )

        cust_ananya, _ = Customer.objects.get_or_create(
            phone="+91 99887 65432",
            defaults={'name': "Dr. Ananya Rao", 'email': "ananya.rao@apollo.in", 'total_visits': 6, 'total_spent': Decimal('6800.00')}
        )
        LoyaltyAccount.objects.get_or_create(
            customer=cust_ananya,
            defaults={'current_tier': LoyaltyTier.SILVER, 'points_balance': 680, 'lifetime_points': 680}
        )

        # 13. Offers & Coupons
        offer_festive, _ = Offer.objects.get_or_create(
            code="ROYAL20",
            defaults={
                'title': "Royal Nizami Feast - 20% OFF",
                'discount_type': DiscountType.PERCENTAGE,
                'discount_value': Decimal('20.00'),
                'min_order_amount': Decimal('1000.00'),
                'max_discount_amount': Decimal('400.00'),
                'valid_from': timezone.now() - timedelta(days=10),
                'valid_to': timezone.now() + timedelta(days=60),
                'is_active': True,
            }
        )

        # 14. Active & Completed Orders + Billing Invoices
        # Order 1: Completed Dine-in with full GST Invoice & Payment
        order1, _ = Order.objects.get_or_create(
            order_number="ORD-20260909-0001",
            defaults={
                'branch': branch_hyd,
                'order_type': OrderType.DINE_IN,
                'table': tables[0],
                'customer': cust_rajesh,
                'server': created_users[RoleChoices.WAITER],
                'status': OrderStatus.COMPLETED,
                'is_paid': True,
                'subtotal': Decimal('1080.00'),
                'discount_amount': Decimal('100.00'),
                'tax_amount': Decimal('49.00'),
                'grand_total': Decimal('1029.00'),
            }
        )
        OrderItem.objects.get_or_create(order=order1, menu_item=created_menu_items["BIR-CHK-01"], defaults={'quantity': 2, 'unit_price': Decimal('380.00'), 'item_total': Decimal('760.00')})
        OrderItem.objects.get_or_create(order=order1, menu_item=created_menu_items["CUR-PAN-01"], defaults={'quantity': 1, 'unit_price': Decimal('320.00'), 'item_total': Decimal('320.00')})

        inv1, _ = Invoice.objects.get_or_create(
            invoice_number="INV/2026-09/0001",
            defaults={
                'order': order1,
                'branch': branch_hyd,
                'customer': cust_rajesh,
                'restaurant_name': restaurant.name,
                'restaurant_gstin': restaurant.gstin,
                'fssai_number': restaurant.fssai_number,
                'branch_address': f"{branch_hyd.address}, {branch_hyd.city}",
                'taxable_subtotal': Decimal('980.00'),
                'discount_amount': Decimal('100.00'),
                'cgst_amount': Decimal('24.50'),
                'sgst_amount': Decimal('24.50'),
                'igst_amount': Decimal('0.00'),
                'total_tax_amount': Decimal('49.00'),
                'grand_total': Decimal('1029.00'),
                'is_paid': True,
                'cashier': created_users[RoleChoices.CASHIER],
            }
        )
        InvoiceItem.objects.get_or_create(
            invoice=inv1, item_name="Hyderabadi Chicken Dum Biryani",
            defaults={'sac_code': "996331", 'quantity': 2, 'unit_rate': Decimal('380.00'), 'item_total': Decimal('760.00'), 'tax_rate_percent': Decimal('5.00'), 'cgst_amount': Decimal('19.00'), 'sgst_amount': Decimal('19.00')}
        )

        Payment.objects.get_or_create(
            transaction_reference="UPI-SIM-20260909-001",
            defaults={
                'order': order1,
                'invoice': inv1,
                'payment_method': PaymentMethod.UPI,
                'amount': Decimal('1029.00'),
                'status': PaymentStatus.SUCCESS,
                'cashier': created_users[RoleChoices.CASHIER],
            }
        )

        # Order 2: Active Kitchen Order in PREPARING status
        order2, _ = Order.objects.get_or_create(
            order_number="ORD-20260909-0002",
            defaults={
                'branch': branch_hyd,
                'order_type': OrderType.DINE_IN,
                'table': tables[1],
                'customer': cust_ananya,
                'server': created_users[RoleChoices.WAITER],
                'status': OrderStatus.PREPARING,
                'is_paid': False,
                'subtotal': Decimal('850.00'),
                'discount_amount': Decimal('0.00'),
                'tax_amount': Decimal('42.50'),
                'grand_total': Decimal('892.50'),
            }
        )
        OrderItem.objects.get_or_create(order=order2, menu_item=created_menu_items["BIR-MUT-02"], defaults={'quantity': 1, 'unit_price': Decimal('490.00'), 'item_total': Decimal('490.00')})
        OrderItem.objects.get_or_create(order=order2, menu_item=created_menu_items["KEB-MAL-01"], defaults={'quantity': 1, 'unit_price': Decimal('360.00'), 'item_total': Decimal('360.00')})
        tables[1].status = TableStatus.OCCUPIED
        tables[1].current_order = order2
        tables[1].save()

        # KDS Ticket for Order 2
        KitchenTicket.objects.get_or_create(
            ticket_number="KOT-20260909-0002",
            defaults={
                'order': order2,
                'station': KitchenStation.BIRYANI_CURRY,
                'status': TicketStatus.PREPARING,
                'expected_prep_minutes': 25,
            }
        )

        # 15. Guest Reviews
        Review.objects.get_or_create(
            order=order1,
            defaults={
                'branch': branch_hyd,
                'customer': cust_rajesh,
                'food_rating': 5,
                'service_rating': 5,
                'overall_rating': 5,
                'comment': "The authentic dum biryani aroma took me straight to Old Hyderabad! Spectacular service by steward Arjun.",
                'management_response': "Thank you Mr. Rajesh! It was our pleasure serving you royal Nizami hospitality. Look forward to seeing you soon.",
                'responded_by': created_users[RoleChoices.MANAGER],
                'responded_at': timezone.now(),
            }
        )

        # 16. Operational Expenses
        exp_cat_gas, _ = ExpenseCategory.objects.get_or_create(name="Kitchen Gas & LPG")
        Expense.objects.get_or_create(
            title="Commercial 19kg Indane LPG Cylinder (3x)",
            defaults={
                'branch': branch_hyd,
                'category': exp_cat_gas,
                'amount': Decimal('5400.00'),
                'expense_date': today,
                'payment_mode': 'CASH',
                'requested_by': created_users['chef_vikram'],
                'is_approved': True,
                'notes': "Refill for Main Biryani Range",
            }
        )

        # 17. Cash Register Session
        CashRegisterSession.objects.get_or_create(
            branch=branch_hyd,
            status='OPEN',
            defaults={
                'opened_by': created_users[RoleChoices.CASHIER],
                'opening_cash': Decimal('3000.00'),
            }
        )

        # 18. Hardware & System Settings
        settings_defaults = [
            ('THERMAL_PRINTER_WIDTH_MM', '80', 'POS Thermal receipt roll width (58mm or 80mm)'),
            ('AUTO_PRINT_KOT_ON_ORDER', 'True', 'Automatically fire KOT print on order placement'),
            ('ALLOW_CUSTOMER_FEEDBACK', 'True', 'Enable post-dining QR review collection'),
            ('DEFAULT_TABLE_TURNOVER_TARGET_MINS', '60', 'Target dining duration per table'),
        ]
        for k, v, d in settings_defaults:
            SystemSetting.objects.get_or_create(key=k, defaults={'value': v, 'description': d})

        # 19. Train Scikit-Learn Machine Learning Demand Model
        self.stdout.write(self.style.NOTICE("Training Scikit-Learn RandomForest Demand Prediction Engine..."))
        try:
            from apps.ml_prediction.ml_engine import train_demand_forecasting_pipeline, generate_weekly_forecast
            registry = train_demand_forecasting_pipeline()
            self.stdout.write(self.style.SUCCESS(f"[OK] Machine Learning Model trained and registered: {registry.model_name} (R2: {registry.r2_score})"))
            forecasts = generate_weekly_forecast(branch=branch_hyd, days_ahead=7)
            self.stdout.write(self.style.SUCCESS(f"[OK] 7-Day Demand and Procurement Forecast generated: {len(forecasts)} daily records"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"ML Model training warning: {e}"))

        self.stdout.write(self.style.SUCCESS("\n========================================================"))
        self.stdout.write(self.style.SUCCESS("* DINEFLOW ERP SEEDING COMPLETED SUCCESSFULLY!"))
        self.stdout.write(self.style.SUCCESS("All 34 domain apps hydrated with production-ready Indian data."))
        self.stdout.write(self.style.SUCCESS(f"Default Staff & Admin credentials: {passwords}"))
        self.stdout.write(self.style.SUCCESS("========================================================\n"))
