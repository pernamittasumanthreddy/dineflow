"""Sales URL Routing."""
from django.urls import path
from apps.sales import views

app_name = 'sales'

urlpatterns = [
    path('', views.sales_dashboard_view, name='dashboard'),
    path('register/', views.cash_register_view, name='register'),
    path('z-report/', views.daily_z_report_view, name='z_report'),
]
