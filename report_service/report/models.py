from django.db import models


class GenreStat(models.Model):
    genre = models.CharField(max_length=255)
    count = models.IntegerField()


class UserStat(models.Model):
    user_id = models.BigIntegerField()
    taken_count = models.IntegerField()
    expired_count = models.IntegerField()
    in_time = models.IntegerField()
