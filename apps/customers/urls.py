"""Customers URL Routing."""
from django.urls import path
from apps.customers import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list_view, name='list'),
    path('<int:customer_id>/', views.customer_detail_view, name='detail'),
]
