"""Comprehensive Test Suite for Statutory PDF, Excel, and CSV Report Export Services."""
from decimal import Decimal
from datetime import date
from django.test import TestCase
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.inventory.models import IngredientCategory, Ingredient
from apps.orders.models import Order, OrderStatus, OrderType
from apps.billing.models import Invoice
from apps.reports.services import (
    generate_sales_pdf,
    generate_gstr1_excel,
    generate_inventory_valuation_excel,
    generate_sales_csv,
    generate_inventory_valuation_csv,
    generate_gstr1_b2c_csv
)

class ReportServicesTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="reports@royalnizam.in",
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
            order_number="ORD-CSV-01",
            branch=self.branch,
            subtotal=Decimal('1000.00'),
            tax_amount=Decimal('50.00'),
            discount_amount=Decimal('0.00'),
            grand_total=Decimal('1050.00'),
            status=OrderStatus.COMPLETED
        )
        self.invoice = Invoice.objects.create(
            invoice_number="INV/CSV/01",
            order=self.order,
            branch=self.branch,
            restaurant_name=self.restaurant.name,
            restaurant_gstin=self.restaurant.gstin,
            fssai_number=self.restaurant.fssai_number,
            branch_address=self.branch.address,
            taxable_subtotal=Decimal('1000.00'),
            cgst_amount=Decimal('25.00'),
            sgst_amount=Decimal('25.00'),
            total_tax_amount=Decimal('50.00'),
            grand_total=Decimal('1050.00'),
            is_paid=True
        )
        cat = IngredientCategory.objects.create(name="Dairy")
        self.ing = Ingredient.objects.create(
            branch=self.branch,
            category=cat,
            name="Paneer Malai",
            code="ING-PAN",
            unit="kg",
            current_stock=Decimal('20.000'),
            minimum_stock_level=Decimal('10.000'),
            unit_cost=Decimal('300.00')
        )

    def test_generate_sales_pdf(self):
        """Test sales PDF buffer contains non-empty binary content starting with %PDF."""
        today = date.today()
        pdf_buf = generate_sales_pdf(today, today, branch=self.branch)
        data = pdf_buf.read()
        self.assertTrue(len(data) > 0)
        self.assertTrue(data.startswith(b'%PDF'))

    def test_generate_gstr1_excel(self):
        """Test GSTR-1 Excel buffer contains non-empty binary content."""
        today = date.today()
        excel_buf = generate_gstr1_excel(today, today, branch=self.branch)
        data = excel_buf.read()
        self.assertTrue(len(data) > 0)
        self.assertTrue(data.startswith(b'PK'))  # Zip-compressed XLSX signature

    def test_generate_inventory_valuation_excel(self):
        """Test inventory valuation Excel buffer contains valid XLSX data."""
        excel_buf = generate_inventory_valuation_excel(branch=self.branch)
        data = excel_buf.read()
        self.assertTrue(len(data) > 0)
        self.assertTrue(data.startswith(b'PK'))

    def test_generate_sales_csv(self):
        """Test sales CSV output contains order number and monetary columns."""
        today = date.today()
        csv_data = generate_sales_csv(today, today, branch=self.branch)
        self.assertIn("ORD-CSV-01", csv_data)
        self.assertIn("1000.00", csv_data)
        self.assertIn("1050.00", csv_data)

    def test_generate_inventory_valuation_csv(self):
        """Test inventory valuation CSV contains SKU, stock, unit cost, and total value."""
        csv_data = generate_inventory_valuation_csv(branch=self.branch)
        self.assertIn("ING-PAN", csv_data)
        self.assertIn("Paneer Malai", csv_data)
        self.assertIn("300.00", csv_data)
        self.assertIn("6000.00", csv_data)

    def test_generate_gstr1_b2c_csv(self):
        """Test statutory GSTR-1 CSV output contains GSTIN, SAC taxable value, and CGST/SGST."""
        today = date.today()
        csv_data = generate_gstr1_b2c_csv(today.month, today.year, branch=self.branch)
        self.assertIn("INV/CSV/01", csv_data)
        self.assertIn("36AAACN1234F1Z9", csv_data)
        self.assertIn("25.00", csv_data)
        self.assertIn("1050.00", csv_data)
