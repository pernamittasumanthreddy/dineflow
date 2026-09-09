from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('invoices/', views.invoices, name='invoices'),
    path('day-end-zreport/', views.day_end_zreport, name='day_end_zreport'),
]
