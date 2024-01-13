from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    user_age = models.DateField(blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    user_height = models.FloatField(blank=True, null=True)
    user_weight = models.FloatField(blank=True, null=True)
    user_activity = models.CharField(max_length=255, blank=True, null=True)
    user_daily_calorie = models.IntegerField(blank=True, null=True)
    user_target_weight = models.IntegerField(blank=True, null=True)

# class UsersAppUser(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#     user_age = models.DateField(blank=True, null=True)
#     user_gender = models.IntegerField(blank=True, null=True)
#     user_height = models.FloatField(blank=True, null=True)
#     user_weight = models.FloatField(blank=True, null=True)
#     user_activity = models.CharField(max_length=255, blank=True, null=True)
#     user_daily_calorie = models.IntegerField(blank=True, null=True)
#     user_target_weight = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users_app_user'