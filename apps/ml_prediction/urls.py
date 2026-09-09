"""ML Prediction URL Routing."""
from django.urls import path
from apps.ml_prediction import views

app_name = 'ml_prediction'

urlpatterns = [
    path('', views.forecast_dashboard_view, name='forecast'),
    path('train/', views.trigger_training_view, name='train'),
]
