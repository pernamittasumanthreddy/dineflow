"""Payments URL Routing."""
from django.urls import path
from apps.payments import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list_view, name='list'),
    path('checkout/<int:order_id>/', views.process_payment_view, name='checkout'),
]
