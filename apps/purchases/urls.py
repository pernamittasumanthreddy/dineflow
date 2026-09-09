"""Purchases URL Routing."""
from django.urls import path
from apps.purchases import views

app_name = 'purchases'

urlpatterns = [
    path('', views.po_list_view, name='list'),
    path('create/', views.po_create_view, name='create'),
    path('<int:po_id>/', views.po_detail_view, name='detail'),
    path('<int:po_id>/receive/', views.po_receive_goods_view, name='receive'),
]
