from django.db import models
from jsonfield import JSONField


class Candle(models.Model):
    asset_class = models.CharField(max_length=10)
    data = models.JSONField()
    date_added = models.DateField()
