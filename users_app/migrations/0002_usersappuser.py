# Generated by Django 4.2.8 on 2024-01-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsersAppUser",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("password", models.CharField(max_length=128)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("is_superuser", models.IntegerField()),
                ("username", models.CharField(max_length=150, unique=True)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.CharField(max_length=254)),
                ("is_staff", models.IntegerField()),
                ("is_active", models.IntegerField()),
                ("date_joined", models.DateTimeField()),
                ("user_age", models.DateField(blank=True, null=True)),
                ("user_gender", models.IntegerField(blank=True, null=True)),
                ("user_height", models.FloatField(blank=True, null=True)),
                ("user_weight", models.FloatField(blank=True, null=True)),
                (
                    "user_activity",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("user_daily_calorie", models.IntegerField(blank=True, null=True)),
                ("user_target_weight", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "users_app_user",
                "managed": False,
            },
        ),
    ]
