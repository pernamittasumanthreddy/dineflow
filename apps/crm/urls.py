from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('loyalty/', views.loyalty_points, name='loyalty_points'),
    path('offers/', views.offers_coupons, name='offers_coupons'),
    path('reviews/', views.reviews_feedback, name='reviews_feedback'),
]
