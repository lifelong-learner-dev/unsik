from django.db import models

class UsersAppUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_birth = models.DateField(blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    user_height = models.FloatField(blank=True, null=True)
    user_weight = models.FloatField(blank=True, null=True)
    user_activity = models.CharField(max_length=255, blank=True, null=True)
    user_daily_calorie = models.IntegerField(blank=True, null=True)
    user_target_weight = models.IntegerField(blank=True, null=True)
    user_exercise_purpose = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_app_user'

class Point(models.Model):
    point_idx = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
    point = models.IntegerField()
    gaining_method = models.CharField(max_length=30, blank=True, null=True)
    gained_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'point'