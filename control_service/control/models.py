from django.db import models


class UserMonitoring(models.Model):
    user_id = models.BigIntegerField()
    max_count = models.IntegerField()
    current_count = models.IntegerField()
