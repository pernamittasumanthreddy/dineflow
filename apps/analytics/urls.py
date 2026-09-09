from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('bi/', views.business_bi, name='business_bi'),
    path('ml-demand/', views.ml_demand, name='ml_demand'),
    path('tax-reports/', views.tax_reports, name='tax_reports'),
]
