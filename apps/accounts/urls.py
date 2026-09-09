"""Accounts App Routing."""
from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/toggle-lock/', views.user_toggle_lock_view, name='user_toggle_lock'),
    path('login-history/', views.login_history_view, name='login_history'),
]
