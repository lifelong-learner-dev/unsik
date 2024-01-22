from django.urls import path
from . import views

urlpatterns = [
    path("", views.exercise_index, name='exercise_index'),
    path('record/', views.record_exercise, name='record_exercise'),
]