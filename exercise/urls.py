from django.urls import path
from . import views

urlpatterns = [
    path('record_exercise/', views.record_exercise, name='record_exercise'),
    path("", views.exercise_index, name='exercise_index'),
]