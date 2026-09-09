from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.ledger, name='ledger_root'),
    path('ledger/', views.ledger, name='ledger'),
]
