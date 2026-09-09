"""Loyalty URL Routing."""
from django.urls import path
from apps.loyalty import views

app_name = 'loyalty'

urlpatterns = [
    path('', views.loyalty_dashboard_view, name='dashboard'),
]
