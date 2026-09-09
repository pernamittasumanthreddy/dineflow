"""Reviews URL Routing."""
from django.urls import path
from apps.reviews import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list_view, name='list'),
    path('<int:review_id>/reply/', views.review_reply_view, name='reply'),
]
