"""Audit URL Routing."""
from django.urls import path
from apps.audit import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_log_list_view, name='list'),
]
