from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import json
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
            Candle.objects.filter(asset_class='stock', symbol=symbol.upper()).delete()
            response = r.text
            Candle.objects.create(symbol=symbol.upper(), asset_class='stock', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)

def crypto_candles(request, symbol):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='crypto', symbol=symbol.upper(), date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')
        if r.status_code == 200:
            Candle.objects.filter(asset_class='crypto', symbol=symbol.upper()).delete()
            response = r.text

            Candle.objects.create(symbol=symbol.upper(), asset_class='crypto', data=response)
        else:
            return HttpResponse(status=r.status_code)

    r2 = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')

    list = json.loads(r2.text)

    print("type \/")
    print(type(list))
    # fmt = [float(item) for item in list[0]]
    
    data = []
    for item in list:
        print(item)
        # data.append([item[0]])
        # data.append([float(item[1])])
        # data.append([float(item[2])])
        # data.append([float(item[3])])
        # data.append([float(item[4])])

        data.append([item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])
        # data.append([item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])

    # return HttpResponse(fmt)
    return HttpResponse(json.dumps(data))

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
            Candle.objects.filter(asset_class='forex', symbol=pair.upper()).delete()
            response = r.text
            Candle.objects.create(symbol=pair.upper(), asset_class='forex', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)