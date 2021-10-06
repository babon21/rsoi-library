from django.db import models


class Rating(models.Model):
    user_id = models.BigIntegerField()
    rating = models.IntegerField()
