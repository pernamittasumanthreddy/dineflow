from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('branches/', views.branches, name='branches'),
    path('roles-permissions/', views.roles_permissions, name='roles_permissions'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('backup-restore/', views.backup_restore, name='backup_restore'),
    path('general/', views.general, name='general'),
]
