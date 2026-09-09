"""Orders App URL Routing."""
from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list_view, name='list'),
    path('pos/', views.pos_terminal_view, name='pos'),
    path('<int:order_id>/', views.order_detail_view, name='detail'),
    path('<int:order_id>/status/', views.order_update_status_view, name='update_status'),
    path('<int:order_id>/cancel/', views.order_cancel_view, name='cancel'),
]
