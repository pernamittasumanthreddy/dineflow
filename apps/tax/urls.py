"""Tax URL Routing."""
from django.urls import path
from apps.tax import views

app_name = 'tax'

urlpatterns = [
    path('', views.tax_category_list_view, name='list'),
]
