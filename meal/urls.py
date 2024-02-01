from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal_index, name='meal_index'),
    path("meal_analyze", views.meal_analyze, name='meal_analyze'),
    path("meal_to_analyze", views.meal_to_analyze, name='meal_to_analyze'),
    path("meal_nutrient", views.meal_post, name="meal_nutrient"),
    path("meal_recommend", views.meal_recommend, name='meal_recommend'),
    path("meal_history", views.meal_history, name='meal_history'),
    path('meal_history/<int:year>/<int:month>/', views.get_monthly_history, name='get_monthly_history'),
    path("meal_detail/<str:date>", views.meal_detail, name='meal_detail'),  
    path("calorie_dict", views.calorie_dict, name='calorie_dict'),
    path("calorie_dict/<str:food_code>/", views.food_detail, name='food_detail'),
    path("food_search", views.food_search, name="food_search"),
    path("test", views.test, name='test'),
]