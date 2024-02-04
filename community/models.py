# from django.db import models

# class Point(models.Model):
#     point_idx = models.BigIntegerField(primary_key=True)
#     user = models.ForeignKey('UsersAppUser', models.DO_NOTHING)
#     point = models.IntegerField()
#     gaining_method = models.CharField(max_length=30, blank=True, null=True)
#     gained_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'point'