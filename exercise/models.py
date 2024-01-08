from django.db import models

# Create your models here.
class Exercise(models.Model):
    postnum = models.BigIntegerField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING, blank=True, null=True)
    exercise_date = models.DateField(blank=True, null=True)
    calories_burned = models.FloatField(blank=True, null=True)
    exercise_type = models.CharField(max_length=30, blank=True, null=True)
    exercise_name = models.CharField(max_length=30, blank=True, null=True)
    exercise_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercise'

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