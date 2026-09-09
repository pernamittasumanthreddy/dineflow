from django.urls import path
from . import views

app_name = 'tax_mgmt'

urlpatterns = [
    path('', views.gst_slabs, name='gst_slabs_root'),
    path('gst-slabs/', views.gst_slabs, name='gst_slabs'),
]
