"""
Automated Test Suite for DineFlow - Restaurant ERP & Management System.
Tests all 10 Role Dashboards, 35+ Modules, Template Tags, and AJAX Role Switchers.
"""
from django.test import TestCase, Client
from django.urls import reverse
from dineflow_core.templatetags.dineflow_tags import inr_format, status_class, diet_badge
import json

class DineFlowERPTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page(self):
        """Test public landing page renders successfully with canvas and Indian branding."""
        response = self.client.get(reverse('landing:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DineFlow')
        self.assertContains(response, 'df-spice-canvas')
        self.assertContains(response, '₹185 Cr+')
        self.assertContains(response, '35+ Enterprise Modules')

    def test_all_10_role_dashboards(self):
        """Verify all 10 dedicated role-based dashboards return HTTP 200 with rich content."""
        dashboards = [
            ('dashboard:super_admin', 'Super Admin SaaS Multi-Tenant Center'),
            ('dashboard:owner', 'Executive Command Dashboard'),
            ('dashboard:manager', 'General Manager Floor Operations'),
            ('dashboard:kitchen', 'Kitchen Display System (KDS) & Chef Station'),
            ('dashboard:waiter', 'Captain & Waiter Ordering Terminal'),
            ('dashboard:cashier', 'Cashier Settlement & Daily Collection'),
            ('dashboard:inventory', 'Raw Material Inventory & Stock Control'),
            ('dashboard:hr', 'Human Resources & Staff Payroll'),
            ('dashboard:customer', 'Guest Experience & DineClub Rewards'),
            ('dashboard:analytics', 'Multi-Branch Business Intelligence & AI Forecast'),
        ]
        for url_name, expected_title in dashboards:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_title)

    def test_pos_terminal(self):
        """Test live touch POS terminal layout, categories, and cart."""
        response = self.client.get(reverse('pos:terminal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Touch POS Terminal')
        self.assertContains(response, 'Hyderabadi Chicken Dum Biryani')
        self.assertContains(response, 'df-pos-cart-panel')

    def test_kds_screen(self):
        """Test fullscreen Kitchen Display System."""
        response = self.client.get(reverse('kds:live'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'KDS Live Cooking Queue')

    def test_all_core_modules(self):
        """Test full availability of all operational ERP modules."""
        modules = [
            'tables:floor_plan',
            'tables:reservations',
            'menu:item_list',
            'menu:categories',
            'menu:recipe_costing',
            'orders:live_orders',
            'delivery:fleet',
            'inventory:stock_ledger',
            'inventory:purchase_orders',
            'inventory:waste_log',
            'suppliers:list',
            'billing:invoices',
            'billing:day_end_zreport',
            'hr:employee_list',
            'hr:attendance',
            'hr:shifts',
            'hr:payroll',
            'crm:customer_list',
            'crm:loyalty_points',
            'crm:offers_coupons',
            'crm:reviews_feedback',
            'expenses:ledger',
            'tax_mgmt:gst_slabs',
            'analytics:business_bi',
            'analytics:ml_demand',
            'analytics:tax_reports',
            'settings_app:branches',
            'settings_app:roles_permissions',
            'settings_app:audit_logs',
            'settings_app:backup_restore',
            'settings_app:general',
            'accounts:login',
            'accounts:register',
            'accounts:forgot_password',
            'accounts:otp_verify',
            'accounts:session_timeout',
        ]
        for mod_url in modules:
            with self.subTest(module=mod_url):
                response = self.client.get(reverse(mod_url))
                self.assertEqual(response.status_code, 200)

    def test_role_switcher_api(self):
        """Test AJAX session role switching endpoint."""
        response = self.client.post(
            reverse('accounts:switch_role_api'),
            data=json.dumps({'role': 'kitchen'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['redirect_url'], '/dashboard/kitchen/')

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

    def test_logout_view(self):
        """Test sign out endpoint clears session and redirects to login with confirmation."""
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/?signed_out=1', response.url)

