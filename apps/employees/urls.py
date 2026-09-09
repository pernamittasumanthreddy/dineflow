"""Employees URL Routing."""
from django.urls import path
from apps.employees import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list_view, name='list'),
    path('<int:employee_id>/', views.employee_detail_view, name='detail'),
]
