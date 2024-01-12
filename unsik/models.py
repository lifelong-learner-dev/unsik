from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     pass

class UsersAppUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=18, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=18, blank=True, null=True)
    profile_img = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    user_age = models.DateField(blank=True, null=True)
    user_height = models.FloatField(blank=True, null=True)
    user_weight = models.FloatField(blank=True, null=True)
    user_activity = models.CharField(max_length=255, blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    user_target_weight = models.IntegerField(blank=True, null=True)
    user_daily_calorie = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_app_user'