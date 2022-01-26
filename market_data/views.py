from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def stock_candles(request, symbol):
    return HttpResponse("You're looking at symbol %s." % symbol)