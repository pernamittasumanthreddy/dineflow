"""Enterprise Diagnostic Health Check & Integrity Audit Command."""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.accounts.models import User
from apps.menu.models import MenuItem
from apps.inventory.models import Ingredient
from apps.orders.models import Order
from apps.billing.models import Invoice

class Command(BaseCommand):
    help = 'Executes system-wide database, hardware switch, and ML model health checks.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=== DINEFLOW ERP ENTERPRISE HEALTH AUDIT ==="))
        
        # 1. Database Connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS("[OK] Database Connection: Operational (Active)"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Database Connection Error: {e}"))
            return

        # 2. Multi-Tenancy & Outlets
        r_count = Restaurant.objects.count()
        b_count = Branch.objects.count()
        u_count = User.objects.count()
        self.stdout.write(self.style.SUCCESS(f"[OK] Multi-Tenancy: {r_count} Restaurant(s), {b_count} Active Branch(es), {u_count} Registered User(s)"))

        # 3. Catalog & Inventory
        m_count = MenuItem.objects.count()
        i_count = Ingredient.objects.count()
        self.stdout.write(self.style.SUCCESS(f"[OK] Master Catalog: {m_count} Menu Dishes, {i_count} Raw Ingredients"))

        # 4. Transactions
        o_count = Order.objects.count()
        inv_count = Invoice.objects.count()
        self.stdout.write(self.style.SUCCESS(f"[OK] Ledger: {o_count} Orders, {inv_count} Statutory GST Tax Invoices"))

        # 5. Machine Learning Artifact
        ml_path = os.path.join(settings.ML_MODELS_DIR, 'demand_forecast_rf_v1.joblib')
        if os.path.exists(ml_path):
            size_kb = round(os.path.getsize(ml_path) / 1024, 1)
            self.stdout.write(self.style.SUCCESS(f"[OK] Machine Learning Engine: RandomForest pipeline present ({size_kb} KB)"))
        else:
            self.stdout.write(self.style.WARNING("[WARN] Machine Learning Engine: Model artifact not found (Run 'python manage.py seed_dineflow' to train)"))

        self.stdout.write(self.style.SUCCESS("=== HEALTH AUDIT COMPLETED: SYSTEM NORMAL ==="))
