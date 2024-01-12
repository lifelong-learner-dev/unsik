from django.urls import path, include
from . import views

# app_name = 'users_app'

urlpatterns = [
    path("sign_up", views.sign_up, name="sign_up"),
    path("id_check", views.id_check, name='id_check'),
    path("sign_in", views.sign_in, name='sign_in'),
    path("sign_out", views.sign_out, name='sign_out')
]