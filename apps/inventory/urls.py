"""Inventory App URL Routing."""
from django.urls import path
from apps.inventory import views

app_name = 'inventory'

urlpatterns = [
    path('', views.stock_list_view, name='stock_list'),
    path('adjust/<int:ingredient_id>/', views.stock_adjust_view, name='adjust'),
    path('movements/', views.stock_movements_view, name='movements'),
]
