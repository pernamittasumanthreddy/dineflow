from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.fleet, name='fleet_root'),
    path('fleet/', views.fleet, name='fleet'),
]
