"""Restaurants URL routing."""
from django.urls import path
from apps.restaurants import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_profile_view, name='profile_root'),
    path('profile/', views.restaurant_profile_view, name='profile'),
]
