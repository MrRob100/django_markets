from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import os

# Create your views here.

def stock_candles(request, symbol):

    headers = {
        'APCA-API-KEY-ID': os.environ.get('ALPACA_KEY'),
        'APCA-API-SECRET-KEY': os.environ.get('ALPACA_SECRET')
    }

    r = requests.get('https://data.alpaca.markets/v2/stocks/' + symbol + '/bars', headers=headers)
    print(os.environ.get('ALPACA_KEY'))

#     return HttpResponse(json.dumps(r))
    return HttpResponse("You're looking at symbol %s." % r.status_code)

def crypto_candles(request, symbol):



    return HttpResponse("You're looking at symbol " + symbol)
#     return HttpResponse("You're looking at symbol %s." % symbol)

def forex_candles(request, symbol):



    return HttpResponse("You're looking at symbol " + symbol)
#     return HttpResponse("You're looking at symbol %s." % symbol)