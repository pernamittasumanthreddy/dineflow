from django.urls import path
from . import views

app_name = 'kds'

urlpatterns = [
    path('', views.live_kds, name='live'),
]
