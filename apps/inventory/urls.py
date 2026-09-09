from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.stock_ledger, name='stock_ledger_root'),
    path('stock-ledger/', views.stock_ledger, name='stock_ledger'),
    path('purchase-orders/', views.purchase_orders, name='purchase_orders'),
    path('waste-log/', views.waste_log, name='waste_log'),
]
