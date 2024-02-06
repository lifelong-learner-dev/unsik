from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Community(models.Model):
    postnum = models.BigAutoField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING, blank=True, null=True)      
    category = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    post_date = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'community'


class Reply(models.Model):
    replyno = models.BigAutoField(db_column='replyNo', primary_key=True)  # Field name made lowercase.
    postnum = models.ForeignKey(Community, models.CASCADE, db_column='postNum', related_name='fk_reply_community')  # Field name made lowercase.
    user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
    reply = models.TextField(blank=True, null=True)
    post_date = models.DateTimeField(default=datetime.datetime.now)
    adopt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reply'

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