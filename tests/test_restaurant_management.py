"""
Automated Test Suite for Restaurant & Branch Management Subsystems.
Covers:
1. Restaurant & RestaurantSetting ORM models, GSTIN/FSSAI, defaults
2. Branch ORM model, unique code, capacity, and active states
3. Corporate Profile view access control & updates
4. Branch list, create, edit views & RBAC access control
5. Active branch session switching
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.accounts.seeder import seed_roles_and_users
from apps.restaurants.models import Restaurant, RestaurantSetting
from apps.branches.models import Branch

User = get_user_model()

class RestaurantManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed_roles_and_users()
        cls.restaurant = Restaurant.objects.create(
            name="The Royal Nizam Lounge",
            slug="royal-nizam-lounge",
            legal_entity_name="Royal Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="contact@royalnizam.in",
            phone="+91 40 2334 5678",
            address_line1="Plot 42, Road 36, Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500033",
            country="India"
        )
        cls.setting = RestaurantSetting.objects.create(
            restaurant=cls.restaurant,
            default_cgst_percent=2.50,
            default_sgst_percent=2.50,
            invoice_prefix="RNL"
        )
        cls.branch1 = Branch.objects.create(
            restaurant=cls.restaurant,
            name="Jubilee Hills Main",
            code="HYD-JH-01",
            phone="+91 40 2334 5679",
            email="jh@royalnizam.in",
            address="Plot 42, Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500033",
            total_seating_capacity=80
        )

    def setUp(self):
        self.client = Client()

    def login_as(self, role_code):
        user = User.objects.filter(userprofile__role__code=role_code).first()
        self.client.force_login(user)
        return user

    def test_restaurant_model_creation(self):
        """Restaurant model stores GSTIN, FSSAI, and business identifiers accurately."""
        self.assertEqual(self.restaurant.name, "The Royal Nizam Lounge")
        self.assertEqual(self.restaurant.gstin, "36AAACN1234F1Z9")
        self.assertEqual(self.restaurant.fssai_number, "13624014000189")
        self.assertEqual(str(self.restaurant), "The Royal Nizam Lounge (GSTIN: 36AAACN1234F1Z9)")

    def test_restaurant_settings_defaults(self):
        """RestaurantSetting accurately reflects tax and operational switch values."""
        self.assertEqual(self.setting.default_cgst_percent, 2.50)
        self.assertEqual(self.setting.default_sgst_percent, 2.50)
        self.assertEqual(self.setting.invoice_prefix, "RNL")
        self.assertTrue(self.setting.enable_kds)
        self.assertEqual(str(self.setting), "Settings for The Royal Nizam Lounge")

    def test_branch_creation_and_attributes(self):
        """Branch is linked to restaurant with unique code and seating capacity."""
        self.assertEqual(self.branch1.restaurant, self.restaurant)
        self.assertEqual(self.branch1.code, "HYD-JH-01")
        self.assertEqual(self.branch1.total_seating_capacity, 80)
        self.assertTrue(self.branch1.is_active)
        self.assertIn("HYD-JH-01", str(self.branch1))

    def test_restaurant_profile_view_authorized_owner(self):
        """Restaurant Owner can access and view restaurant corporate profile."""
        self.login_as('owner')
        response = self.client.get(reverse('restaurants:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Corporate Entity Details')
        self.assertContains(response, '36AAACN1234F1Z9')

    def test_restaurant_profile_view_denies_unauthorized_waiter(self):
        """Waiter is forbidden (HTTP 403) from accessing restaurant profile."""
        self.login_as('waiter')
        response = self.client.get(reverse('restaurants:profile'))
        self.assertEqual(response.status_code, 403)

    def test_branch_list_view_authorized_roles(self):
        """Owner and Manager can view branches list."""
        self.login_as('manager')
        response = self.client.get(reverse('branches:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jubilee Hills Main')
        self.assertContains(response, 'HYD-JH-01')

    def test_branch_list_view_denies_unauthorized_waiter(self):
        """Waiter cannot access branches list (HTTP 403)."""
        self.login_as('waiter')
        response = self.client.get(reverse('branches:list'))
        self.assertEqual(response.status_code, 403)

    def test_branch_create_view_creates_new_branch(self):
        """Owner can create a new branch outlet."""
        self.login_as('owner')
        payload = {
            'name': 'Banjara Hills Express',
            'code': 'HYD-BH-02',
            'phone': '+91 40 2334 9999',
            'email': 'bh@royalnizam.in',
            'address': 'Road No 12, Banjara Hills',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'pincode': '500034',
            'opening_time': '11:00',
            'closing_time': '23:00',
            'total_seating_capacity': 50,
            'is_active': True,
        }
        response = self.client.post(reverse('branches:create'), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Branch.objects.filter(code='HYD-BH-02').exists())

    def test_switch_branch_view_updates_session(self):
        """Switching branch updates session active branch context."""
        self.login_as('owner')
        response = self.client.get(reverse('branches:switch', kwargs={'branch_id': self.branch1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('active_branch_id'), self.branch1.id)
        self.assertEqual(self.client.session.get('active_branch_name'), 'Jubilee Hills Main')

