from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('role-select/', views.role_select_view, name='role_select'),
    path('login/', views.login_view, name='login'),
    path('login/<str:role_code>/', views.login_view, name='login_role'),
    path('logout/', views.logout_view, name='logout'),
    path('signout/', views.logout_view, name='signout'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('session-timeout/', views.session_timeout_view, name='session_timeout'),
]
