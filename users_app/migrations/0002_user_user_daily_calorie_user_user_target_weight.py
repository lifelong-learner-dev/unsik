# Generated by Django 4.2.8 on 2024-01-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_daily_calorie",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="user_target_weight",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
