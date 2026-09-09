"""ML Prediction Django Admin."""
from django.contrib import admin
from apps.ml_prediction.models import PredictionModelRegistry, DailyDemandForecast, IngredientRequirementForecast

class IngredientRequirementForecastInline(admin.TabularInline):
    model = IngredientRequirementForecast
    extra = 0
    readonly_fields = ('ingredient', 'predicted_quantity', 'unit', 'estimated_cost')

@admin.register(PredictionModelRegistry)
class PredictionModelRegistryAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'version', 'algorithm', 'r2_score', 'mae_score', 'training_sample_count', 'is_active', 'created_at')
    list_filter = ('model_type', 'is_active')

@admin.register(DailyDemandForecast)
class DailyDemandForecastAdmin(admin.ModelAdmin):
    list_display = ('target_date', 'branch', 'predicted_order_count', 'predicted_guest_covers', 'predicted_sales_revenue', 'confidence_score')
    list_filter = ('branch', 'target_date')
    inlines = [IngredientRequirementForecastInline]
