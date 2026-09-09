from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('live/', views.live_orders, name='live_orders'),
]
