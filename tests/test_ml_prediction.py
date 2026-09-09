"""Comprehensive Test Suite for Scikit-Learn Machine Learning Demand Forecasting."""
import os
from decimal import Decimal
from django.test import TestCase
from django.conf import settings
from apps.restaurants.models import Restaurant
from apps.branches.models import Branch
from apps.inventory.models import IngredientCategory, Ingredient
from apps.ml_prediction.models import PredictionModelRegistry, DailyDemandForecast, IngredientRequirementForecast
from apps.ml_prediction.ml_engine import (
    generate_synthetic_training_dataset,
    train_demand_forecasting_pipeline,
    generate_weekly_forecast
)

class MLPredictionTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="The Royal Nizam",
            legal_entity_name="Nizam Hospitality Pvt Ltd",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="ai@royalnizam.in",
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
        cat = IngredientCategory.objects.create(name="Grains")
        self.rice = Ingredient.objects.create(
            branch=self.branch,
            category=cat,
            name="Aged Basmati Rice",
            code="ING-RIC",
            unit="kg",
            current_stock=Decimal('100.000'),
            minimum_stock_level=Decimal('30.000')
        )

    def test_synthetic_training_dataset_generation(self):
        """Test generating synthetic restaurant traffic and order datasets with seasonality features."""
        df = generate_synthetic_training_dataset(sample_size=100)
        self.assertEqual(len(df), 100)
        required_cols = {'day_of_week', 'is_weekend', 'month', 'guest_covers', 'order_count', 'sales_revenue'}
        self.assertTrue(required_cols.issubset(set(df.columns)))
        # Order count should always be positive
        self.assertTrue((df['order_count'] > 0).all())

    def test_train_demand_forecasting_pipeline(self):
        """Test training the Scikit-Learn RandomForestRegressor and saving registry metadata."""
        registry = train_demand_forecasting_pipeline()
        self.assertIsNotNone(registry)
        self.assertEqual(registry.model_name, 'DineFlow Guest Traffic Forecaster')
        self.assertTrue(registry.is_active)
        self.assertGreaterEqual(registry.r2_score, -1.0)
        self.assertTrue(os.path.exists(registry.artifact_path))

    def test_generate_weekly_forecast(self):
        """Test executing inference to generate 7-day daily demand projections."""
        train_demand_forecasting_pipeline()
        forecasts = generate_weekly_forecast(branch=self.branch, days_ahead=7)
        self.assertEqual(len(forecasts), 7)
        
        first_day = forecasts[0]
        self.assertGreater(first_day.predicted_order_count, 0)
        self.assertGreater(first_day.predicted_guest_covers, 0)
        self.assertGreater(first_day.predicted_sales_revenue, Decimal('0.00'))
