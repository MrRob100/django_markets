from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import json
from grpc import StatusCode
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
    record = Candle.objects.filter(
        asset_class='crypto', symbol=symbol, date_added__gt=time_threshold)

    if record.exists():
        candles = record.latest('data').data
    else:
        Candle.objects.filter(asset_class='crypto', symbol=symbol).delete()
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')
        if r.status_code == 200:
            response = r.text
            list = json.loads(response)

            data = []
            for item in list:
                data.append([item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])

            candles = json.dumps(data)
            Candle.objects.create(symbol=symbol.upper(), asset_class='crypto', data=candles)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(candles)

# def forex_candles(request, pair):
#     time_threshold = datetime.now() - timedelta(hours=5)
#     record = Candle.objects.filter(asset_class='forex', symbol=pair, date_added__gt=time_threshold)

#     if record.exists():
#         response = record.latest('data').data
#     else:
#         end = int(time.time())
#         start = end - 331556952
#         token = os.environ.get('FINNHUB_KEY')
#         formatted = pair[:3] + '-' + pair[3:]
#         r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:' + formatted.upper() + '&resolution=D&from' + str(start) + '&to=' + str(end) + '&token=' + token)
#         if r.status_code == 200:
#             Candle.objects.filter(asset_class='forex', symbol=pair.upper()).delete()
#             response = r.text
#             Candle.objects.create(symbol=pair.upper(), asset_class='forex', data=response)
#         else:
#             return HttpResponse(status=r.status_code)

#     return HttpResponse(response)


def forex_candles(request, pair):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(
        asset_class='forexFFFF', symbol=pair, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + pair[:3].upper() + 'USDT&interval=1d')
        r2 = requests.get('https://www.binance.com/api/v3/klines?symbol=' + pair[3:].upper() + 'USDT&interval=1d')

        if r.status_code == 200 and r2.status_code == 200:
            list1 = json.loads(r.text)
            list2 = json.loads(r2.text)    
            if len(list1) < len(list2):
                shortest = list1
                longest = list2
            else:
                shortest = list2
                longest = list1

            i = 0
            combined = []
            for item in shortest:
                combined.append(
                    [
                        item[0], 
                        float(item[1]) / float(longest[i][1]), 
                        float(item[2]) / float(longest[i][2]),
                        float(item[3]) / float(longest[i][3]),
                        float(item[4]) / float(longest[i][4])
                    ]
                )
                i = i+1

            Candle.objects.filter(asset_class='forex', symbol=pair.upper()).delete()
            response = combined
            Candle.objects.create(symbol=pair.upper(), asset_class='forex', data=combined)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)
