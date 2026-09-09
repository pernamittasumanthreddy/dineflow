"""Suppliers URL Routing."""
from django.urls import path
from apps.suppliers import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.supplier_list_view, name='list'),
    path('create/', views.supplier_create_view, name='create'),
    path('<int:supplier_id>/', views.supplier_detail_view, name='detail'),
]
