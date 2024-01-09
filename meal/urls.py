from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal_index, name='meal_index'),
    path("meal_analyze", views.meal_analyze, name='meal_analyze'),
    path("calorie_dict", views.calorie_dict, name='calorie_dict'),
    path("calorie_dict/<str:food_code>/", views.food_detail, name='food_detail')
]