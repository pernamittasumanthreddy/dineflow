"""Comprehensive Test Suite for Diagnostic and Statutory Management Commands."""
from io import StringIO
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.orders.models import Order
from apps.billing.models import Invoice

class ManagementCommandsTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="ops@royalnizam.in",
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
        self.order = Order.objects.create(
            order_number="ORD-CMD-01",
            branch=self.branch,
            subtotal=Decimal('1000.00'),
            grand_total=Decimal('1050.00'),
            is_paid=True
        )
        self.invoice = Invoice.objects.create(
            invoice_number="INV/CMD/01",
            order=self.order,
            branch=self.branch,
            taxable_subtotal=Decimal('1000.00'),
            cgst_amount=Decimal('25.00'),
            sgst_amount=Decimal('25.00'),
            total_tax_amount=Decimal('50.00'),
            grand_total=Decimal('1050.00'),
            is_paid=True
        )

    def test_check_dineflow_health_command(self):
        """Test check_dineflow_health diagnostic outputs operational status."""
        out = StringIO()
        call_command('check_dineflow_health', stdout=out)
        output = out.getvalue()
        self.assertIn("DINEFLOW ERP ENTERPRISE HEALTH AUDIT", output)
        self.assertIn("[OK] Database Connection: Operational", output)
        self.assertIn("Multi-Tenancy", output)
        self.assertIn("Master Catalog", output)

    def test_export_gst_summary_command(self):
        """Test export_gst_summary aggregates statutory GST collections."""
        out = StringIO()
        now = timezone.localdate()
        call_command('export_gst_summary', month=now.month, year=now.year, stdout=out)
        output = out.getvalue()
        self.assertIn("STATUTORY INDIAN GST RETURN SUMMARY", output)
        self.assertIn("Central GST (CGST 2.5%)", output)
        self.assertIn("State GST   (SGST 2.5%)", output)
        self.assertIn("Total Settled Tax Invoices", output)
