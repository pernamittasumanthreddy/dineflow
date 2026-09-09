"""Comprehensive Test Suite for Internal Notification Engine Services."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.inventory.models import IngredientCategory, Ingredient
from apps.orders.models import Order, OrderStatus, OrderType
from apps.payments.models import Payment, PaymentMethod, PaymentStatus
from apps.notifications.models import Notification, NotificationType
from apps.notifications.services import (
    send_low_stock_notification,
    send_new_order_notification,
    send_payment_received_notification,
    mark_all_notifications_read
)

User = get_user_model()

class NotificationServicesTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="notif@royalnizam.in",
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
        self.manager = User.objects.create_user(
            email="manager.notif@dineflow.in",
            username="mgr_notif",
            password="ManagerPassword123!"
        )
        cat = IngredientCategory.objects.create(name="Grains")
        self.ingredient = Ingredient.objects.create(
            branch=self.branch,
            category=cat,
            name="Basmati Rice",
            unit="kg",
            current_stock=Decimal('15.000'),
            minimum_stock_level=Decimal('30.000')
        )
        self.order = Order.objects.create(
            order_number="ORD-NOTIF-01",
            branch=self.branch,
            grand_total=Decimal('850.00'),
            guest_count=3
        )
        self.payment = Payment.objects.create(
            order=self.order,
            amount=Decimal('850.00'),
            payment_method=PaymentMethod.UPI,
            status=PaymentStatus.SUCCESS
        )

    def test_send_low_stock_notification(self):
        """Test generating low-stock alert."""
        notif = send_low_stock_notification(self.ingredient, recipient=self.manager)
        self.assertEqual(notif.notification_type, NotificationType.LOW_STOCK)
        self.assertIn("Basmati Rice", notif.title)
        self.assertFalse(notif.is_read)

    def test_send_new_order_notification(self):
        """Test generating new order notification."""
        notif = send_new_order_notification(self.order, recipient=self.manager)
        self.assertEqual(notif.notification_type, NotificationType.NEW_ORDER)
        self.assertIn("ORD-NOTIF-01", notif.title)
        self.assertIn("850.00", notif.message)

    def test_send_payment_received_notification(self):
        """Test generating payment receipt notification."""
        notif = send_payment_received_notification(self.payment, recipient=self.manager)
        self.assertEqual(notif.notification_type, NotificationType.PAYMENT)
        self.assertIn("850.00", notif.title)

    def test_mark_all_notifications_read(self):
        """Test bulk updating user notifications to read."""
        send_low_stock_notification(self.ingredient, recipient=self.manager)
        send_new_order_notification(self.order, recipient=self.manager)
        
        unread_count = Notification.objects.filter(recipient=self.manager, is_read=False).count()
        self.assertEqual(unread_count, 2)

        updated = mark_all_notifications_read(self.manager)
        self.assertEqual(updated, 2)
        
        remaining_unread = Notification.objects.filter(recipient=self.manager, is_read=False).count()
        self.assertEqual(remaining_unread, 0)
