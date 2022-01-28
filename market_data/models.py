from django.db import models
from jsonfield import JSONField
from datetime import datetime

class Candle(models.Model):
    symbol = models.CharField(max_length=10)
    asset_class = models.CharField(max_length=10)
    data = models.JSONField()
    date_added = models.DateTimeField(auto_now=True)

    def __str_(self):
        return self.symbol