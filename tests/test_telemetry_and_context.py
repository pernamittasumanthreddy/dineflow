"""Comprehensive Test Suite for Request Telemetry, Security Headers & Global Context Processors."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.core.middleware import RequestTimingMiddleware, SecurityHeaderMiddleware
from apps.core.context_processors import dineflow_global_context

User = get_user_model()

class TelemetryAndContextTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="telemetry@royalnizam.in",
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
        self.user = User.objects.create_user(
            email="user.telemetry@dineflow.in",
            username="user_telem",
            password="UserPassword123!",
            branch=self.branch,
            restaurant=self.restaurant
        )

    def test_request_timing_middleware_header(self):
        """Test middleware calculates duration and sets X-Response-Time-Ms header."""
        def dummy_view(req):
            return HttpResponse("OK")

        middleware = RequestTimingMiddleware(dummy_view)
        request = self.factory.get('/test/')
        response = middleware(request)

        self.assertIn('X-Response-Time-Ms', response)
        ms_val = float(response['X-Response-Time-Ms'])
        self.assertGreaterEqual(ms_val, 0.0)

    def test_security_header_middleware(self):
        """Test security middleware injects nosniff, SAMEORIGIN, and Referrer-Policy."""
        def dummy_view(req):
            return HttpResponse("OK")

        middleware = SecurityHeaderMiddleware(dummy_view)
        request = self.factory.get('/test/')
        response = middleware(request)

        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['X-Frame-Options'], 'SAMEORIGIN')
        self.assertEqual(response['Referrer-Policy'], 'strict-origin-when-cross-origin')

    def test_dineflow_global_context_processor(self):
        """Test global context processor injects active branch and server clock."""
        request = self.factory.get('/test/')
        request.user = self.user

        context = dineflow_global_context(request)
        self.assertIn('current_server_time', context)
        self.assertIn('app_name', context)
        self.assertEqual(context['app_name'], 'DineFlow Enterprise ERP')
        self.assertEqual(context['active_branch'], self.branch)
        self.assertIn('pending_kds_count', context)
        self.assertIn('low_stock_count', context)
        self.assertIn('unread_notif_count', context)
