"""Core App URL Configuration."""
from django.urls import path
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home_redirect_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
