from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('profile/', views.profile_view, name='profile'),
    path('switch-role/', views.switch_role_api, name='switch_role_api'),
    path('switch-branch/', views.switch_branch_api, name='switch_branch_api'),
    path('session-timeout/', views.session_timeout_view, name='session_timeout'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
]
