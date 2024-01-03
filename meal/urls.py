from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal_index, name='meal_index'),
]