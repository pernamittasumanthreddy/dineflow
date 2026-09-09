"""
URL configuration for dineflow project.
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

# Customize Admin Site Branding
admin.site.site_header = "DineFlow Restaurant ERP & Database Portal"
admin.site.site_title = "DineFlow ERP"
admin.site.index_title = "DineFlow Enterprise Database & Management System"

urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False), name='home_redirect'),
    path('admin/', admin.site.urls),
]
