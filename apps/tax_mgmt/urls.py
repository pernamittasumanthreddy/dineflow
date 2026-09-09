from django.urls import path
from . import views

app_name = 'tax_mgmt'

urlpatterns = [
    path('gst-slabs/', views.gst_slabs, name='gst_slabs'),
]
