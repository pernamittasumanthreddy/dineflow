"""Tables URL routing."""
from django.urls import path
from apps.tables import views

app_name = 'tables'

urlpatterns = [
    path('', views.floor_plan_view, name='floor_plan'),
    path('create/', views.table_create_view, name='table_create'),
    path('<int:table_id>/status/', views.table_toggle_status_view, name='table_toggle_status'),
]
