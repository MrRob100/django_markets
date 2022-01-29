from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import requests
import os
from .models import Candle


def stock_candles(request, symbol):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='stock', symbol=symbol, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        headers = {
            'APCA-API-KEY-ID': os.environ.get('ALPACA_KEY'),
            'APCA-API-SECRET-KEY': os.environ.get('ALPACA_SECRET')
        }

        start = (datetime.today() - timedelta(days=200)).date()
        end = (datetime.today() - timedelta(days=1)).date()
        r = requests.get('https://data.alpaca.markets/v2/stocks/' + symbol + '/bars?timeframe=1Day&start=' + str(start) + '&end=' + str(end), headers=headers)
        if r.status_code == 200:
            response = r.text
            Candle.objects.create(symbol=symbol.upper(), asset_class='stock', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)

def crypto_candles(request, symbol):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='crypto', symbol=symbol, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        Candle.objects.filter(asset_class='crypto', symbol=symbol).delete()
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')
        if r.status_code == 200:
            response = r.text
            Candle.objects.create(symbol=symbol.upper(), asset_class='crypto', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)

def forex_candles(request, pair):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='forex', symbol=pair, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        end = int(time.time())
        start = end - 331556952
        token = os.environ.get('FINNHUB_KEY')
        formatted = pair[:3] + '-' + pair[3:]
        r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:' + formatted.upper() + '&resolution=D&from' + str(start) + '&to=' + str(end) + '&token=' + token)
        if r.status_code == 200:
            response = r.text
            Candle.objects.create(symbol=pair.upper(), asset_class='forex', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)