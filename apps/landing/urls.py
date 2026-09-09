from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.index, name='index'),
    path('landing/', views.index, name='landing_page'),
]
