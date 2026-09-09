"""Attendance URL Routing."""
from django.urls import path
from apps.attendance import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list_view, name='list'),
    path('punch/', views.time_clock_view, name='punch'),
]
