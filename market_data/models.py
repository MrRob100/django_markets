from django.db import models
from jsonfield import JSONField

class Candle(models.Model):
    symbol = models.CharField(max_length=10)
    asset_class = models.CharField(max_length=10)
    data = models.JSONField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

class SymbolList(models.Model):
    symbols = models.JSONField()
    asset_class = models.CharField(max_length=10)
    source = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asset_class + ' (' + self.source + ')'