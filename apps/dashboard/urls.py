from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('super-admin/', views.super_admin_dashboard, name='super_admin'),
    path('owner/', views.owner_dashboard, name='owner'),
    path('manager/', views.manager_dashboard, name='manager'),
    path('kitchen/', views.kitchen_dashboard, name='kitchen'),
    path('waiter/', views.waiter_dashboard, name='waiter'),
    path('cashier/', views.cashier_dashboard, name='cashier'),
    path('inventory/', views.inventory_dashboard, name='inventory'),
    path('hr/', views.hr_dashboard, name='hr'),
    path('customer/', views.customer_dashboard, name='customer'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
]
