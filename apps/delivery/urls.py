"""Delivery URL Routing."""
from django.urls import path
from apps.delivery import views

app_name = 'delivery'

urlpatterns = [
    path('', views.delivery_board_view, name='board'),
    path('<int:delivery_id>/assign/', views.delivery_assign_rider_view, name='assign'),
    path('<int:delivery_id>/status/', views.delivery_status_update_view, name='status_update'),
]
