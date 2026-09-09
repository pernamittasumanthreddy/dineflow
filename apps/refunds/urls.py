"""Refunds URL Routing."""
from django.urls import path
from apps.refunds import views

app_name = 'refunds'

urlpatterns = [
    path('', views.refund_list_view, name='list'),
    path('request/<int:payment_id>/', views.refund_request_view, name='request'),
    path('<int:refund_id>/approval/', views.refund_approval_view, name='approval'),
]
