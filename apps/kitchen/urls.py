"""Kitchen App URL Routing."""
from django.urls import path
from apps.kitchen import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.kds_board_view, name='kds'),
    path('bump/<int:ticket_id>/', views.ticket_bump_view, name='bump'),
    path('performance/', views.kitchen_performance_view, name='performance'),
]
