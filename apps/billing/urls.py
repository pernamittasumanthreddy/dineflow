from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.invoices, name='invoices_root'),
    path('invoices/', views.invoices, name='invoices'),
    path('z-report/', views.day_end_zreport, name='day_end_zreport'),
    path('day-end-zreport/', views.day_end_zreport, name='z_report'),
]
