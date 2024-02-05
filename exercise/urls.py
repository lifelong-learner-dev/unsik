from django.urls import path
from . import views

urlpatterns = [
    path('record_exercise/', views.record_exercise, name='record_exercise'),
    # path("", views.exercise_index, name='exercise_index'),
    path('exercises/<str:date>/', views.get_exercises_for_date, name='get_exercises_for_date'),
    # path('exercises/', views.get_exercises_for_date, name='get_exercises_for_date'),
    path('exercise/index/', views.exercise_index, name='exercise_index'),
    # path('exercise/search/', views.exercise_search, name='exercise_search'),
    path('exercise/edit/<int:id>/', views.exercise_edit, name='exercise_edit'),
    path('exercise/delete/<int:id>/', views.exercise_delete, name='exercise_delete'),
    path('record_exercise/predict_calories/', views.predict_calories, name='predict_calories'),
    # path('record_exercise/predict_calories/', views.test, name='test'),
]