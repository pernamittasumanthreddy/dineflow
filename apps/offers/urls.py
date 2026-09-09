"""Offers URL Routing."""
from django.urls import path
from apps.offers import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list_view, name='list'),
    path('validate/', views.validate_coupon_api, name='validate'),
]
