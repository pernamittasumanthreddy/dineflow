"""Reports URL Routing."""
from django.urls import path
from apps.reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index_view, name='index'),
    path('sales-pdf/', views.export_sales_pdf_view, name='sales_pdf'),
    path('gstr1-excel/', views.export_gstr1_excel_view, name='gstr1_excel'),
    path('inventory-excel/', views.export_inventory_excel_view, name='inventory_excel'),
]
