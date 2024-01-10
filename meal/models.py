from django.db import models

# Create your models here.
class Meal(models.Model):
    postnum = models.BigIntegerField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
    meal_date = models.DateTimeField(blank=True, null=True)
    meal_photo = models.CharField(max_length=255, blank=True, null=True)
    meal_info = models.TextField(blank=True, null=True)
    meal_type = models.CharField(max_length=20, blank=True, null=True)
    meal_calories = models.FloatField(blank=True, null=True)
    nutrient_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meal'

class CalorieDictionary(models.Model):
    food_code = models.CharField(primary_key=True, max_length=10)
    food_name = models.CharField(max_length=100)
    maker = models.CharField(max_length=100)
    major_class = models.CharField(max_length=50)
    detail_class = models.CharField(max_length=50)
    one_serve_amount_g_field = models.FloatField(db_column='one_serve_amount(g)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    total_amount_g_field = models.FloatField(db_column='total_amount(g)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    calories = models.FloatField(blank=True, null=True)
    water = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carbohydrate = models.FloatField(blank=True, null=True)
    suger = models.FloatField(blank=True, null=True)
    dietary_fiber = models.FloatField(blank=True, null=True)
    natrium = models.FloatField(blank=True, null=True)
    total_sfa = models.FloatField(blank=True, null=True)
    total_tfa = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calorie_dictionary'

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