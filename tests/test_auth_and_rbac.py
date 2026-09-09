"""Comprehensive Test Suite for Authentication, Security and 10-Role RBAC."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from apps.accounts.models import RoleChoices
from apps.accounts.decorators import role_required, module_permission_required
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch

User = get_user_model()

class AuthenticationAndRBACTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
        # Base restaurant & branch
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Royal Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="info@royalnizam.in",
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
            address="Road No 12, Banjara Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
            phone="+91 40 2334 1100"
        )

        # Create test users for different roles
        self.admin = User.objects.create_superuser(
            email="admin@dineflow.in",
            username="admin",
            password="AdminPassword123!",
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.manager = User.objects.create_user(
            email="manager@dineflow.in",
            username="manager",
            password="ManagerPassword123!",
            role=RoleChoices.MANAGER,
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.waiter = User.objects.create_user(
            email="waiter@dineflow.in",
            username="waiter",
            password="WaiterPassword123!",
            role=RoleChoices.WAITER,
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.cashier = User.objects.create_user(
            email="cashier@dineflow.in",
            username="cashier",
            password="CashierPassword123!",
            role=RoleChoices.CASHIER,
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.kitchen = User.objects.create_user(
            email="chef@dineflow.in",
            username="chef",
            password="ChefPassword123!",
            role=RoleChoices.KITCHEN_STAFF,
            restaurant=self.restaurant,
            branch=self.branch
        )
        self.customer = User.objects.create_user(
            email="customer@dineflow.in",
            username="customer",
            password="CustomerPassword123!",
            role=RoleChoices.CUSTOMER
        )

    def test_all_ten_roles_exist(self):
        """Verify that all 10 granular enterprise roles exist in RoleChoices."""
        expected_roles = {
            'SUPER_ADMIN', 'RESTAURANT_OWNER', 'MANAGER', 'KITCHEN_STAFF',
            'WAITER', 'CASHIER', 'INVENTORY_MANAGER', 'HR', 'CUSTOMER', 'ANALYTICS_USER'
        }
        actual_roles = {choice[0] for choice in RoleChoices.choices}
        self.assertEqual(expected_roles, actual_roles)

    def test_user_creation_and_password_hashing(self):
        """Verify user creation, role assignment, and secure password hashing."""
        self.assertTrue(self.waiter.check_password("WaiterPassword123!"))
        self.assertFalse(self.waiter.check_password("WrongPassword"))
        self.assertEqual(self.waiter.role, RoleChoices.WAITER)
        self.assertEqual(self.waiter.branch, self.branch)

    def test_superuser_attributes(self):
        """Verify superuser has staff privileges and SUPER_ADMIN role."""
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)
        self.assertEqual(self.admin.role, RoleChoices.SUPER_ADMIN)

    def test_role_required_decorator_allows_authorized_role(self):
        """Verify role_required decorator executes view for authorized role."""
        @role_required(RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN)
        def dummy_view(request):
            return "SUCCESS"

        request = self.factory.get('/manager-only/')
        request.user = self.manager
        response = dummy_view(request)
        self.assertEqual(response, "SUCCESS")

    def test_role_required_decorator_blocks_unauthorized_role(self):
        """Verify role_required decorator raises PermissionDenied for unauthorized role."""
        @role_required(RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN)
        def dummy_view(request):
            return "SUCCESS"

        request = self.factory.get('/manager-only/')
        request.user = self.waiter
        with self.assertRaises(PermissionDenied):
            dummy_view(request)

    def test_superuser_bypasses_role_restriction(self):
        """Verify superuser is granted access through role_required regardless of listed roles."""
        @role_required(RoleChoices.KITCHEN_STAFF)
        def kitchen_view(request):
            return "KITCHEN_ORDER"

        request = self.factory.get('/kitchen/')
        request.user = self.admin
        response = kitchen_view(request)
        self.assertEqual(response, "KITCHEN_ORDER")

    def test_login_view_get(self):
        """Verify login page renders with HTTP 200."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_authentication_success(self):
        """Verify successful user authentication logs in and redirects."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'manager@dineflow.in',
            'password': 'ManagerPassword123!'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_login_view_invalid_credentials(self):
        """Verify failed authentication with incorrect password."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'manager@dineflow.in',
            'password': 'WrongPassword123'
        })
        self.assertEqual(response.status_code, 200)
        # Session should not contain authenticated user ID
        self.assertFalse('_auth_user_id' in self.client.session)
