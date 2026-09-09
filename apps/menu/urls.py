from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('items/', views.item_list, name='item_list'),
    path('categories/', views.categories, name='categories'),
    path('recipe-costing/', views.recipe_costing, name='recipe_costing'),
]
