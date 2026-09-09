"""Reservations URL Routing."""
from django.urls import path
from apps.reservations import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list_view, name='list'),
    path('create/', views.reservation_create_view, name='create'),
    path('<int:reservation_id>/status/', views.reservation_status_update_view, name='status_update'),
]
