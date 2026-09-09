"""Comprehensive Test Suite for System Settings Caching & Audit Services."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.settings_manager.models import SystemSetting
from apps.settings_manager.services import (
    get_setting,
    set_setting,
    clear_settings_cache,
    get_thermal_printer_width
)
from apps.audit.models import AuditLog, AuditAction
from apps.audit.services import log_audit_action, get_audit_trail_for_object

User = get_user_model()

class SettingsAndAuditServicesTestCase(TestCase):
    def setUp(self):
        clear_settings_cache()
        self.admin = User.objects.create_superuser(
            email="admin.svc@dineflow.in",
            username="admin_svc",
            password="AdminPassword123!"
        )

    def test_settings_get_set_and_cache(self):
        """Test setting, reading, and caching configuration keys."""
        set_setting('AUTO_KOT_PRINT', 'True', 'Auto print KOT on order placement')
        val = get_setting('AUTO_KOT_PRINT')
        self.assertEqual(val, 'True')

        # Test thermal printer width helper
        set_setting('THERMAL_PRINTER_WIDTH_MM', '80')
        self.assertEqual(get_thermal_printer_width(), 80)

        # Test default fallback
        missing = get_setting('NON_EXISTENT_KEY', default='DEFAULT_VAL')
        self.assertEqual(missing, 'DEFAULT_VAL')

    def test_log_audit_action_service(self):
        """Test creating an audit trail log via log_audit_action service."""
        log = log_audit_action(
            actor=self.admin,
            action=AuditAction.PRICE_CHANGE,
            module_name='menu',
            object_id='BIR-01',
            object_repr='Chicken Biryani',
            old_values={'price': '350.00'},
            new_values={'price': '380.00'},
            ip_address='192.168.1.50'
        )
        self.assertIsNotNone(log)
        self.assertEqual(log.module_name, 'menu')
        self.assertEqual(log.action, AuditAction.PRICE_CHANGE)

        # Retrieve history
        history = get_audit_trail_for_object('menu', 'BIR-01')
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].old_values['price'], '350.00')
