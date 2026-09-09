"""Billing App URL Routing."""
from django.urls import path
from apps.billing import views

app_name = 'billing'

urlpatterns = [
    path('', views.invoice_list_view, name='list'),
    path('generate/<int:order_id>/', views.generate_invoice_for_order_view, name='generate'),
    path('<int:invoice_id>/', views.invoice_detail_view, name='detail'),
    path('<int:invoice_id>/thermal/', views.thermal_receipt_view, name='thermal'),
]
