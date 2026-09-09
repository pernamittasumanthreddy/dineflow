from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.floor_plan, name='floor_plan_root'),
    path('floor-plan/', views.floor_plan, name='floor_plan'),
    path('reservations/', views.reservations, name='reservations'),
]
