from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.employee_list, name='employee_list_root'),
    path('employees/', views.employee_list, name='employee_list'),
    path('attendance/', views.attendance, name='attendance'),
    path('shifts/', views.shifts, name='shifts'),
    path('payroll/', views.payroll, name='payroll'),
]
