"""Menu URL Routing."""
from django.urls import path
from apps.menu import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_catalog_view, name='catalog'),
    path('items/create/', views.menu_item_create_view, name='item_create'),
    path('items/<int:item_id>/edit/', views.menu_item_edit_view, name='item_edit'),
    path('items/<int:item_id>/toggle-availability/', views.menu_item_toggle_availability_view, name='item_toggle_availability'),
    path('categories/', views.category_list_view, name='category_list'),
]
