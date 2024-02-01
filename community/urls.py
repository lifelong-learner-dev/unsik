from django.urls import path
from . import views

urlpatterns = [
    path("", views.fitness_grade, name='fitness_grade'),   
    path("male_senior_predict_ajax/", views.male_senior_predict_ajax, name='male_senior_predict_ajax'),
    path("female_senior_predict_ajax/", views.female_senior_predict_ajax, name='female_senior_predict_ajax'),
    path("male_adult_predict_ajax/", views.male_adult_predict_ajax, name='male_adult_predict_ajax'),
    path("female_adult_predict_ajax/", views.female_adult_predict_ajax, name='female_adult_predict_ajax'),
    path("male_adolescent_predict_ajax/", views.male_adolescent_predict_ajax, name='male_adolescent_predict_ajax'),
    path("female_adolescent_predict_ajax/", views.female_adolescent_predict_ajax, name='female_adolescent_predict_ajax'),
    path("male_child_predict_ajax/", views.male_child_predict_ajax, name='male_child_predict_ajax'),
    path("female_child_predict_ajax/", views.female_child_predict_ajax, name='female_child_predict_ajax'),
    path("llm/", views.llm_index, name='llm_index'),
    path("healthcareassistant/", views.healthcareassistant, name='healthcareassistant')
]