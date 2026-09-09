"""
DineFlow Database Seeder: Seeds all 10 Enterprise Roles and standard pre-configured test users.
"""
from django.contrib.auth.models import User
from apps.accounts.models import Role, UserProfile, Permission, RolePermission

ROLE_DEFINITIONS = [
    {
        'code': 'super_admin',
        'name': 'Super Admin',
        'description': 'Multi-Tenant SaaS Management & Cloud Infrastructure',
        'dashboard_url': '/dashboard/super-admin/',
        'icon': '🛡️',
        'username': 'superadmin',
        'email': 'superadmin@dineflow.in',
        'full_name': 'Kavita Sundaram',
        'phone': '+91 98450 11001',
        'initials': 'KS',
        'emp_code': 'SA-001'
    },
    {
        'code': 'owner',
        'name': 'Restaurant Owner',
        'description': 'Enterprise Chain Financials, P&L & Strategic Decisions',
        'dashboard_url': '/dashboard/owner/',
        'icon': '👑',
        'username': 'owner',
        'email': 'owner@dineflow.in',
        'full_name': 'Vikramaditya Rao',
        'phone': '+91 98450 11002',
        'initials': 'VR',
        'emp_code': 'OWN-001'
    },
    {
        'code': 'manager',
        'name': 'General Manager',
        'description': 'Store Operations, Floor Table Control & Shift Management',
        'dashboard_url': '/dashboard/manager/',
        'icon': '👔',
        'username': 'manager',
        'email': 'manager@dineflow.in',
        'full_name': 'Rajeshwar Reddy',
        'phone': '+91 98450 11003',
        'initials': 'RR',
        'emp_code': 'MGR-002'
    },
    {
        'code': 'kitchen',
        'name': 'Kitchen Staff / Chef',
        'description': 'Live KDS Cooking Stations, KOT Bump & Prep Timers',
        'dashboard_url': '/dashboard/kitchen/',
        'icon': '👨‍🍳',
        'username': 'kitchen',
        'email': 'kitchen@dineflow.in',
        'full_name': 'Chef Sanjeev Kumar',
        'phone': '+91 98450 11004',
        'initials': 'SK',
        'emp_code': 'KTC-011'
    },
    {
        'code': 'waiter',
        'name': 'Waiter / Captain',
        'description': 'Table Ordering, Floor Map & Guest Service Coordination',
        'dashboard_url': '/dashboard/waiter/',
        'icon': '🤵',
        'username': 'waiter',
        'email': 'waiter@dineflow.in',
        'full_name': 'Arun Verma',
        'phone': '+91 98450 11005',
        'initials': 'AV',
        'emp_code': 'WTR-042'
    },
    {
        'code': 'cashier',
        'name': 'Cashier / Billing',
        'description': 'Touch POS, GST Split Invoicing, UPI QR & Day-End Z-Report',
        'dashboard_url': '/dashboard/cashier/',
        'icon': '💵',
        'username': 'cashier',
        'email': 'cashier@dineflow.in',
        'full_name': 'Deepika Sharma',
        'phone': '+91 98450 11006',
        'initials': 'DS',
        'emp_code': 'CSH-008'
    },
    {
        'code': 'inventory',
        'name': 'Inventory Manager',
        'description': 'Raw Material Stock Ledger, Purchase Orders, GRN & Waste',
        'dashboard_url': '/dashboard/inventory/',
        'icon': '📦',
        'username': 'inventory',
        'email': 'inventory@dineflow.in',
        'full_name': 'Manoj Bajpayee',
        'phone': '+91 98450 11007',
        'initials': 'MB',
        'emp_code': 'INV-005'
    },
    {
        'code': 'hr',
        'name': 'HR & Payroll Manager',
        'description': 'Biometric Attendance, Staff Rosters & Indian Statutory Payroll',
        'dashboard_url': '/dashboard/hr/',
        'icon': '👥',
        'username': 'hr',
        'email': 'hr@dineflow.in',
        'full_name': 'Pooja Hegde',
        'phone': '+91 98450 11008',
        'initials': 'PH',
        'emp_code': 'HR-003'
    },
    {
        'code': 'customer',
        'name': 'Customer / Guest',
        'description': 'Digital Dining Menu, Table Bookings & DineClub Rewards',
        'dashboard_url': '/dashboard/customer/',
        'icon': '⭐',
        'username': 'customer',
        'email': 'customer@dineflow.in',
        'full_name': 'Ananya Deshmukh',
        'phone': '+91 98450 11009',
        'initials': 'AD',
        'emp_code': 'GST-881'
    },
    {
        'code': 'analytics',
        'name': 'Analytics & BI Analyst',
        'description': 'Multi-Branch BI Revenue Trends, ML Demand & Tax Reports',
        'dashboard_url': '/dashboard/analytics/',
        'icon': '📈',
        'username': 'analytics',
        'email': 'analytics@dineflow.in',
        'full_name': 'Siddharth Menon',
        'phone': '+91 98450 11010',
        'initials': 'SM',
        'emp_code': 'DAT-004'
    },
]

DEFAULT_PASSWORD = 'DineFlow@2026'

def seed_roles_and_users():
    """
    Ensures all 10 roles and pre-configured enterprise accounts exist in the database.
    """
    for r_def in ROLE_DEFINITIONS:
        role, _ = Role.objects.update_or_create(
            code=r_def['code'],
            defaults={
                'name': r_def['name'],
                'description': r_def['description'],
                'dashboard_url': r_def['dashboard_url'],
                'icon': r_def['icon'],
                'is_active': True,
            }
        )

        user, user_created = User.objects.get_or_create(
            username=r_def['username'],
            defaults={'email': r_def['email']}
        )
        if user_created or not user.has_usable_password():
            user.set_password(DEFAULT_PASSWORD)
            user.first_name = r_def['full_name'].split()[0]
            user.last_name = ' '.join(r_def['full_name'].split()[1:]) if len(r_def['full_name'].split()) > 1 else ''
            user.email = r_def['email']
            user.save()

        # Update or create UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'role': role,
                'branch': 'Indiranagar Main (Bangalore)',
                'employee_code': r_def['emp_code'],
                'phone': r_def['phone'],
                'avatar_initials': r_def['initials'],
            }
        )
