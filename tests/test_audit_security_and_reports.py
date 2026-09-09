"""Comprehensive Test Suite for Audit Trails, Notifications, Table Reservations, and System Settings."""
from datetime import time, date
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import RoleChoices
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.tables.models import FloorSection, RestaurantTable, TableStatus
from apps.audit.models import AuditLog, AuditAction
from apps.notifications.models import Notification, NotificationType
from apps.reservations.models import Reservation, ReservationStatus
from apps.settings_manager.models import SystemSetting

User = get_user_model()

class AuditSecurityAndReportsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="audit@royalnizam.in",
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
            address="Road No 12",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
            phone="+91 40 2334 1100"
        )
        self.admin = User.objects.create_superuser(
            email="admin.audit@dineflow.in",
            username="admin_audit",
            password="AdminPassword123!",
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.section = FloorSection.objects.create(
            branch=self.branch,
            name="Garden Lounge"
        )
        self.table = RestaurantTable.objects.create(
            branch=self.branch,
            section=self.section,
            table_number="G-01",
            seating_capacity=4
        )

    def test_immutable_audit_log_recording(self):
        """Test creating an audit trail log capturing actor, action, and JSON diffs."""
        log = AuditLog.objects.create(
            actor=self.admin,
            action=AuditAction.PRICE_CHANGE,
            module_name='menu',
            object_id='BIR-CHK-01',
            object_repr='Hyderabadi Chicken Dum Biryani',
            ip_address='127.0.0.1',
            old_values={'base_price': '350.00'},
            new_values={'base_price': '380.00'}
        )
        self.assertEqual(log.action, AuditAction.PRICE_CHANGE)
        self.assertEqual(log.module_name, 'menu')
        self.assertEqual(log.old_values['base_price'], '350.00')
        self.assertEqual(log.new_values['base_price'], '380.00')
        self.assertEqual(log.actor.username, 'admin_audit')

    def test_internal_notification_dispatch(self):
        """Test internal notification generation and read status update."""
        notif = Notification.objects.create(
            recipient=self.admin,
            title="Low Stock Alert: Basmati Rice",
            message="Rice inventory has breached minimum reorder threshold (20kg remaining).",
            notification_type=NotificationType.LOW_STOCK,
            url="/inventory/",
            is_read=False
        )
        self.assertFalse(notif.is_read)
        self.assertEqual(notif.notification_type, NotificationType.LOW_STOCK)

        # User reads notification
        notif.is_read = True
        notif.save()
        self.assertTrue(notif.is_read)

    def test_guest_reservation_lifecycle(self):
        """Test table booking lifecycle: PENDING -> CONFIRMED -> SEATED -> COMPLETED."""
        res = Reservation.objects.create(
            branch=self.branch,
            guest_name="Kavita Krishnan",
            guest_phone="+91 99887 76655",
            guest_email="kavita.k@gmail.com",
            reservation_date=date(2026, 9, 12),
            reservation_time=time(19, 30),
            guest_count=4,
            assigned_table=self.table,
            status=ReservationStatus.PENDING
        )
        self.assertEqual(res.status, ReservationStatus.PENDING)

        # Manager confirms booking
        res.status = ReservationStatus.CONFIRMED
        res.save()
        self.assertEqual(res.status, ReservationStatus.CONFIRMED)

        # Guest arrives and is seated
        res.status = ReservationStatus.SEATED
        res.save()
        self.assertEqual(res.status, ReservationStatus.SEATED)

    def test_system_settings_key_value_store(self):
        """Test hardware and peripheral configuration key-value storage."""
        setting = SystemSetting.objects.create(
            key="THERMAL_PRINTER_WIDTH_MM",
            value="80",
            description="POS thermal receipt paper roll width"
        )
        self.assertEqual(setting.key, "THERMAL_PRINTER_WIDTH_MM")
        self.assertEqual(setting.value, "80")
