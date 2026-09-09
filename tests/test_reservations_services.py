"""Comprehensive Test Suite for Table Reservation Conflicts, Capacity, and Seating Workflows."""
from datetime import date, time
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.tables.models import FloorSection, RestaurantTable, TableStatus
from apps.reservations.models import Reservation, ReservationStatus
from apps.reservations.services import (
    book_guest_reservation,
    seat_reservation,
    cancel_or_no_show_reservation,
    check_table_conflict
)
from apps.notifications.models import Notification

class ReservationsServicesTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="reservations@royalnizam.in",
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
        self.section = FloorSection.objects.create(branch=self.branch, name="AC Dining")
        self.table_small = RestaurantTable.objects.create(
            branch=self.branch, section=self.section, table_number="T-02", seating_capacity=2, status=TableStatus.AVAILABLE
        )
        self.table_large = RestaurantTable.objects.create(
            branch=self.branch, section=self.section, table_number="T-06", seating_capacity=6, status=TableStatus.AVAILABLE
        )

    def test_book_reservation_success(self):
        """Test booking a reservation within table capacity."""
        res = book_guest_reservation(
            branch=self.branch,
            guest_name="Sunil Gavaskar",
            guest_phone="+91 98200 11223",
            booking_date=date(2026, 9, 20),
            booking_time=time(19, 0),
            guest_count=4,
            assigned_table=self.table_large
        )
        self.assertEqual(res.status, ReservationStatus.CONFIRMED)
        self.assertEqual(res.assigned_table, self.table_large)
        
        # Internal notification generated
        notif = Notification.objects.filter(title__contains="Sunil Gavaskar").first()
        self.assertIsNotNone(notif)

    def test_book_reservation_capacity_exceeded_raises_error(self):
        """Test trying to seat 4 guests on a 2-person table raises ValidationError."""
        with self.assertRaises(ValidationError):
            book_guest_reservation(
                branch=self.branch,
                guest_name="Kapil Dev",
                guest_phone="+91 98110 33445",
                booking_date=date(2026, 9, 20),
                booking_time=time(19, 0),
                guest_count=4,  # Table only seats 2
                assigned_table=self.table_small
            )

    def test_book_reservation_time_conflict_detected(self):
        """Test booking another reservation on the same table within 90 minutes raises ValidationError."""
        # Booking 1 at 19:00
        book_guest_reservation(
            branch=self.branch,
            guest_name="Guest 1",
            guest_phone="+91 98000 11111",
            booking_date=date(2026, 9, 20),
            booking_time=time(19, 0),
            guest_count=4,
            assigned_table=self.table_large
        )

        # Booking 2 on same table at 19:30 (30 mins diff < 90 mins buffer)
        with self.assertRaises(ValidationError):
            book_guest_reservation(
                branch=self.branch,
                guest_name="Guest 2",
                guest_phone="+91 98000 22222",
                booking_date=date(2026, 9, 20),
                booking_time=time(19, 30),
                guest_count=4,
                assigned_table=self.table_large
            )

    def test_seat_and_free_table_lifecycle(self):
        """Test seating updates reservation status to SEATED and table to OCCUPIED."""
        res = book_guest_reservation(
            branch=self.branch,
            guest_name="Rahul Dravid",
            guest_phone="+91 98450 66778",
            booking_date=date(2026, 9, 20),
            booking_time=time(20, 0),
            guest_count=2,
            assigned_table=self.table_small
        )
        seat_reservation(res)
        self.assertEqual(res.status, ReservationStatus.SEATED)
        self.table_small.refresh_from_db()
        self.assertEqual(self.table_small.status, TableStatus.OCCUPIED)

        # Cancel frees table
        cancel_or_no_show_reservation(res, is_no_show=True)
        self.assertEqual(res.status, ReservationStatus.NO_SHOW)
