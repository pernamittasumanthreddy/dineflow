"""Backups URL Routing."""
from django.urls import path
from apps.backups import views

app_name = 'backups'

urlpatterns = [
    path('', views.backup_list_view, name='list'),
    path('create/', views.backup_create_view, name='create'),
    path('<int:backup_id>/download/', views.backup_download_view, name='download'),
]
