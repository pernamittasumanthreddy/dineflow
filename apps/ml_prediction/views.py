"""Machine Learning Demand Forecasting and Procurement Dashboard Views."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.ml_prediction.models import DailyDemandForecast, PredictionModelRegistry, IngredientRequirementForecast
from apps.ml_prediction.ml_engine import generate_weekly_forecast, train_demand_forecasting_pipeline
from apps.accounts.decorators import module_permission_required

@login_required
def forecast_dashboard_view(request):
    """
    ML Prediction Executive Dashboard.
    Displays 7-day forward forecasts for orders, revenues, and ingredient requirements.
    """
    branch = request.user.branch
    today = timezone.localdate()

    forecasts = DailyDemandForecast.objects.filter(
        target_date__gte=today
    ).select_related('model_used', 'branch').prefetch_related('ingredient_requirements__ingredient')

    if branch:
        forecasts = forecasts.filter(branch=branch)

    # If no future forecasts exist, generate them automatically
    if not forecasts.exists():
        generate_weekly_forecast(branch=branch, days_ahead=7)
        forecasts = DailyDemandForecast.objects.filter(target_date__gte=today)
        if branch:
            forecasts = forecasts.filter(branch=branch)

    forecasts = forecasts.order_by('target_date')[:7]
    active_model = PredictionModelRegistry.objects.filter(is_active=True).first()

    total_projected_revenue = sum(f.predicted_sales_revenue for f in forecasts)
    total_projected_orders = sum(f.predicted_order_count for f in forecasts)

    return render(request, 'ml_prediction/forecast.html', {
        'forecasts': forecasts,
        'active_model': active_model,
        'total_projected_revenue': total_projected_revenue,
        'total_projected_orders': total_projected_orders,
    })

@login_required
@module_permission_required('analytics')
def trigger_training_view(request):
    """Retrain the Scikit-Learn regression model and regenerate predictions."""
    try:
        registry = train_demand_forecasting_pipeline()
        generate_weekly_forecast(branch=request.user.branch, days_ahead=7)
        messages.success(request, f"Model retrained successfully! Version: {registry.version} (R² Score: {registry.r2_score}, MAE: {registry.mae_score})")
    except Exception as e:
        messages.error(request, f"Training failed: {str(e)}")
        
    return redirect('ml_prediction:forecast')
