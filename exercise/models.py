from django.db import models

# Create your models here.
class Exercise(models.Model):
    postnum = models.BigIntegerField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING, blank=True, null=True)
    exercise_date = models.DateTimeField(blank=True, null=True)
    calories_burned = models.FloatField(blank=True, null=True)
    exercise_type = models.CharField(max_length=3, blank=True, null=True)       
    exercise_name = models.CharField(max_length=30, blank=True, null=True)      
    exercise_amount = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercise'

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
    user_age = models.DateField(blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)
    user_height = models.FloatField(blank=True, null=True)
    user_weight = models.FloatField(blank=True, null=True)
    user_activity = models.CharField(max_length=255, blank=True, null=True)     
    user_daily_calorie = models.IntegerField(blank=True, null=True)
    user_target_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_app_user'