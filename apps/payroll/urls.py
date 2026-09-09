"""Payroll URL Routing."""
from django.urls import path
from apps.payroll import views

app_name = 'payroll'

urlpatterns = [
    path('', views.payroll_list_view, name='list'),
    path('generate/', views.payroll_generate_month_view, name='generate'),
    path('<int:payroll_id>/', views.payslip_detail_view, name='payslip'),
    path('<int:payroll_id>/disburse/', views.payroll_disburse_view, name='disburse'),
]
