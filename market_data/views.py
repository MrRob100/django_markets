from django.http import HttpResponse
from django.shortcuts import render
import datetime
import time
import requests
import os
import json
from .models import Candle


def stock_candles(request, symbol):
    headers = {
        'APCA-API-KEY-ID': os.environ.get('ALPACA_KEY'),
        'APCA-API-SECRET-KEY': os.environ.get('ALPACA_SECRET')
    }

    start = (datetime.datetime.today() - datetime.timedelta(days=200)).date()
    end = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
    r = requests.get('https://data.alpaca.markets/v2/stocks/' + symbol + '/bars?timeframe=1Day&start=' + str(start) + '&end=' + str(end), headers=headers)

    return HttpResponse(r.text)

def crypto_candles(request, symbol):

    #add date condition
    record = Candle.objects.filter(asset_class='crypto', symbol=symbol)
    print(record.exists())

    if record.exists():
        response = record.data
    else:
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')
        response = r.text
        Candle.objects.create(symbol=symbol, asset_class='crypto', data=json.dumps(response))


    return HttpResponse(response)

def forex_candles(request, pair):
    end = int(time.time())
    start = end - 331556952
    token = os.environ.get('FINNHUB_KEY')
    formatted = pair[:3] + '-' + pair[3:]
    r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:' + formatted.upper() + '&resolution=D&from' + str(start) + '&to=' + str(end) + '&token=' + token)

    return HttpResponse(r.text)