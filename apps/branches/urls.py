"""Branch URLs."""
from django.urls import path
from apps.branches import views

app_name = 'branches'

urlpatterns = [
    path('', views.branch_list_view, name='list'),
    path('create/', views.branch_create_view, name='create'),
    path('<int:branch_id>/edit/', views.branch_edit_view, name='edit'),
    path('<int:branch_id>/switch/', views.switch_branch_view, name='switch'),
]
