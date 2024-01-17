from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal_index, name='meal_index'),
    path("meal_analyze", views.meal_analyze, name='meal_analyze'),
    path("meal_history", views.meal_history, name='meal_history'),
]