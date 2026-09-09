from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.business_bi, name='business_bi_root'),
    path('bi/', views.business_bi, name='business_bi'),
    path('forecast/', views.ml_demand, name='ml_demand'),
    path('tax/', views.tax_reports, name='tax_reports'),
]
