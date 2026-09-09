"""Shifts URL Routing."""
from django.urls import path
from apps.shifts import views

app_name = 'shifts'

urlpatterns = [
    path('', views.shift_roster_view, name='roster'),
]
