from django.http import HttpResponse
from django.shortcuts import render
import datetime
from datetime import date
import requests
import json
import os

# Create your views here.

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
    r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')

    return HttpResponse(r.text)

def forex_candles(request, symbol):



    return HttpResponse("You're looking at symbol " + symbol)
#     return HttpResponse("You're looking at symbol %s." % symbol)