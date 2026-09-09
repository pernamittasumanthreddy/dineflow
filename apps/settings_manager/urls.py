"""Settings Manager URL Routing."""
from django.urls import path
from apps.settings_manager import views

app_name = 'settings_manager'

urlpatterns = [
    path('', views.settings_overview_view, name='overview'),
]
