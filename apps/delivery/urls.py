from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('fleet/', views.fleet, name='fleet'),
]
