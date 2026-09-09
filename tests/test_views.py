"""
Enterprise Automated Test Suite for DineFlow RBAC & Authentication System.
Validates:
1. Unauthenticated redirects to Role Selection.
2. Role Selection Portal & Role-Specific Login screens.
3. Django Authentication & Role Mismatch Rejections.
4. All 10 Role Logins and Dedicated Dashboards.
5. Strict Module Isolation & HTTP 403 Access Denied.
6. Session Destruction & Real Logout.
7. Template Filters (INR format, Diet badges, Status classes).
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.models import Role, UserProfile
from apps.accounts.seeder import seed_roles_and_users
from dineflow_core.templatetags.dineflow_tags import inr_format, status_class, diet_badge

class DineFlowRBACTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Seed all 10 standard roles and test users
        seed_roles_and_users()

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------
    # 1. Unauthenticated Access & Redirection Tests
    # -------------------------------------------------------------
    def test_root_redirects_unauthenticated_to_role_select(self):
        """Root / must redirect unauthenticated visitors to /accounts/role-select/"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/role-select/', response.url)

    def test_protected_dashboard_redirects_unauthenticated(self):
        """Unauthenticated requests to protected dashboards redirect to role select with next param."""
        response = self.client.get('/dashboard/owner/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/role-select/?next=/dashboard/owner/', response.url)

    def test_role_select_page_renders_all_10_roles(self):
        """Role selection page displays all 10 roles."""
        response = self.client.get(reverse('accounts:role_select'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Super Admin')
        self.assertContains(response, 'Restaurant Owner')
        self.assertContains(response, 'General Manager')
        self.assertContains(response, 'Kitchen Staff / Chef')
        self.assertContains(response, 'Waiter / Captain')
        self.assertContains(response, 'Cashier / Billing')
        self.assertContains(response, 'Inventory Manager')
        self.assertContains(response, 'HR &amp; Payroll Manager')
        self.assertContains(response, 'Customer / Guest')
        self.assertContains(response, 'Analytics &amp; BI Analyst')

    def test_role_login_page_renders_with_selected_role(self):
        """Role-specific login page renders correctly for each role."""
        response = self.client.get(reverse('accounts:login_role', kwargs={'role_code': 'waiter'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Waiter / Captain')
        self.assertContains(response, 'waiter')
        self.assertContains(response, 'DineFlow@2026')

    # -------------------------------------------------------------
    # 2. Authentication & Role Validation Tests
    # -------------------------------------------------------------
    def test_successful_login_redirects_to_role_dashboard(self):
        """Valid credentials matching the selected role log in and redirect to role dashboard."""
        response = self.client.post(
            reverse('accounts:login_role', kwargs={'role_code': 'waiter'}),
            data={'username': 'waiter', 'password': 'DineFlow@2026', 'role_code': 'waiter'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:waiter'))

    def test_role_mismatch_login_rejected(self):
        """Logging in with valid user credentials that DO NOT match the selected role is rejected."""
        # Using cashier user credentials on the waiter login screen
        response = self.client.post(
            reverse('accounts:login_role', kwargs={'role_code': 'waiter'}),
            data={'username': 'cashier', 'password': 'DineFlow@2026', 'role_code': 'waiter'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'These credentials do not belong to the selected role')

    def test_invalid_password_rejected(self):
        """Invalid password displays authentication error."""
        response = self.client.post(
            reverse('accounts:login_role', kwargs={'role_code': 'owner'}),
            data={'username': 'owner', 'password': 'WrongPassword123', 'role_code': 'owner'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username/email or password')

    # -------------------------------------------------------------
    # 3. All 10 Roles Login and Dashboard Access
    # -------------------------------------------------------------
    def test_all_10_roles_login_and_dashboard_access(self):
        """Test that all 10 seeded roles can log in and access their respective dashboards."""
        roles_data = [
            ('super_admin', 'superadmin', reverse('dashboard:super_admin')),
            ('owner', 'owner', reverse('dashboard:owner')),
            ('manager', 'manager', reverse('dashboard:manager')),
            ('kitchen', 'kitchen', reverse('dashboard:kitchen')),
            ('waiter', 'waiter', reverse('dashboard:waiter')),
            ('cashier', 'cashier', reverse('dashboard:cashier')),
            ('inventory', 'inventory', reverse('dashboard:inventory')),
            ('hr', 'hr', reverse('dashboard:hr')),
            ('customer', 'customer', reverse('dashboard:customer')),
            ('analytics', 'analytics', reverse('dashboard:analytics')),
        ]

        for role_code, username, dashboard_url in roles_data:
            with self.subTest(role=role_code):
                client = Client()
                # Post login
                login_resp = client.post(
                    reverse('accounts:login_role', kwargs={'role_code': role_code}),
                    data={'username': username, 'password': 'DineFlow@2026', 'role_code': role_code}
                )
                self.assertEqual(login_resp.status_code, 302)
                self.assertEqual(login_resp.url, dashboard_url)

                # Access dashboard
                dash_resp = client.get(dashboard_url)
                self.assertEqual(dash_resp.status_code, 200)

    # -------------------------------------------------------------
    # 4. Strict RBAC Module Isolation & HTTP 403 Forbidden
    # -------------------------------------------------------------
    def test_waiter_cannot_access_restricted_modules(self):
        """Waiter role cannot access HR Payroll, Settings, or Analytics (returns HTTP 403)."""
        self.client.login(username='waiter', password='DineFlow@2026')

        # Allowed modules for Waiter
        self.assertEqual(self.client.get(reverse('dashboard:waiter')).status_code, 200)
        self.assertEqual(self.client.get(reverse('pos:terminal')).status_code, 200)
        self.assertEqual(self.client.get(reverse('tables:floor_plan')).status_code, 200)

        # Restricted modules for Waiter (Must return 403 Forbidden)
        self.assertEqual(self.client.get(reverse('hr:payroll')).status_code, 403)
        self.assertEqual(self.client.get(reverse('settings_app:branches')).status_code, 403)
        self.assertEqual(self.client.get(reverse('settings_app:backup_restore')).status_code, 403)
        self.assertEqual(self.client.get(reverse('analytics:business_bi')).status_code, 403)
        self.assertEqual(self.client.get(reverse('inventory:stock_ledger')).status_code, 403)

    def test_kitchen_cannot_access_billing_or_payroll(self):
        """Kitchen staff can access KDS but cannot access Billing or HR Payroll (returns HTTP 403)."""
        self.client.login(username='kitchen', password='DineFlow@2026')

        # Allowed for Kitchen
        self.assertEqual(self.client.get(reverse('kds:live')).status_code, 200)
        self.assertEqual(self.client.get(reverse('dashboard:kitchen')).status_code, 200)

        # Restricted for Kitchen
        self.assertEqual(self.client.get(reverse('billing:invoices')).status_code, 403)
        self.assertEqual(self.client.get(reverse('hr:payroll')).status_code, 403)
        self.assertEqual(self.client.get(reverse('settings_app:roles_permissions')).status_code, 403)

    def test_hr_cannot_access_kds_or_backup(self):
        """HR manager can access HR modules but cannot access KDS or Backup Restore."""
        self.client.login(username='hr', password='DineFlow@2026')

        # Allowed for HR
        self.assertEqual(self.client.get(reverse('hr:employee_list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('hr:payroll')).status_code, 200)

        # Restricted for HR
        self.assertEqual(self.client.get(reverse('kds:live')).status_code, 403)
        self.assertEqual(self.client.get(reverse('settings_app:backup_restore')).status_code, 403)

    # -------------------------------------------------------------
    # 5. Real Logout Tests
    # -------------------------------------------------------------
    def test_logout_destroys_session_and_redirects(self):
        """Logging out flushes session and redirects to role selection."""
        self.client.login(username='owner', password='DineFlow@2026')
        self.assertEqual(self.client.get(reverse('dashboard:owner')).status_code, 200)

        # Call logout
        logout_resp = self.client.get(reverse('accounts:logout'))
        self.assertEqual(logout_resp.status_code, 302)
        self.assertIn('/accounts/role-select/?signed_out=1', logout_resp.url)

        # Subsequent request to dashboard is blocked and redirected
        after_logout = self.client.get(reverse('dashboard:owner'))
        self.assertEqual(after_logout.status_code, 302)
        self.assertIn('/accounts/role-select/?next=/dashboard/owner/', after_logout.url)

    # -------------------------------------------------------------
    # 6. Template Tags Tests
    # -------------------------------------------------------------
    def test_inr_currency_formatting(self):
        """Test Indian Rupee formatting template filter."""
        self.assertEqual(inr_format(125000), '₹1,25,000.00')
        self.assertEqual(inr_format(2450), '₹2,450.00')
        self.assertEqual(inr_format(85999), '₹85,999.00')
        self.assertEqual(inr_format(0), '₹0.00')

    def test_status_class_filter(self):
        """Test status class semantic mapping."""
        self.assertEqual(status_class('paid'), 'badge-success')
        self.assertEqual(status_class('preparing'), 'badge-warning')
        self.assertEqual(status_class('urgent'), 'badge-danger')
        self.assertEqual(status_class('low_stock'), 'badge-warning')

    def test_diet_badge_filter(self):
        """Test Indian dietary symbol classification."""
        self.assertEqual(diet_badge('veg'), 'veg-mark')
        self.assertEqual(diet_badge('nonveg'), 'nonveg-mark')
        self.assertEqual(diet_badge('egg'), 'egg-mark')
        self.assertEqual(diet_badge('jain'), 'jain-mark')
