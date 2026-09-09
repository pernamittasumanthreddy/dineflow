from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('floor-plan/', views.floor_plan, name='floor_plan'),
    path('reservations/', views.reservations, name='reservations'),
]
