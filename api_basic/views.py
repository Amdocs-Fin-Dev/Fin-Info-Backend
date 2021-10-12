from enum import Flag
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.functional import new_method_proxy
from numpy import inner
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from .models import Ticket, Mex_stocks
from .serializers import TickerSerializer, Mex_stocks_Serializer
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views import View
from django.db import connection

#APiViews
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#Cosas para la API
import yfinance as yf
import pandas_datareader as pdr
from yfinance import ticker
from os import name, stat
import json
from django.http import JsonResponse

#Tecnical Analysis
import pandas as pd
import ta
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator
from ta.momentum import StochasticOscillator
from ta.volatility import AverageTrueRange

import newsapi
from newsapi.newsapi_client import NewsApiClient
import requests

class TickerAPIView(APIView):
    
    def get(self, request):
        tickers = Ticket.objects.all()
        serializer = TickerSerializer(tickers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TickerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class TickerDetails(APIView):

    def get_object(request, ticker_id):
        try: 
            return Ticket.objects.get(ticker_id=ticker_id)
        except Ticket.DoesNotExist:
            return Response(status= status.HTTP_404_NOT_FOUND)

    def get(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        serializer = TickerSerializer(tick)
        return Response(serializer.data)

    def put(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        serializer = TickerSerializer(tick, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, ticker_id):
        tick = self.get_object(ticker_id)
        tick.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class TickerMostrar(APIView):

    # def get(self, request, ticker_id):
    #     tick = ticker_id
    #     new_ticker = yf.Ticker(tick)
    #     hist = new_ticker.history(period="1mo")
    #     data = hist.to_json()
    #     return JsonResponse(data, safe=False)
    def get(self, request, ticker_id, interval, period):
        #change here to frontend
        tick = "ALSEA.MX"
        #tick = tickerid
        new_ticker = yf.Ticker(ticker_id)
        hist = new_ticker.history(period=period, interval= interval)
        data = hist.to_json()
        return JsonResponse(data, safe=False)
        
    def post(self, request, ticker_id):
        tick = ticker_id
        new_ticker = yf.Ticker(tick)
        hist = new_ticker.history(period="1y")
        data = hist.to_json()
        return JsonResponse(data, safe=False)

class TickerMostrarMonth(View):
#falta interval y tickerid en los parametros
    def get(self, request):
        tick = "ALSEA.MX"
        #tick = tickerid
        interval = "1mo"
        new_ticker = yf.Ticker(tick)
        hist = new_ticker.history(period="1y",interval=interval)
        data = hist.to_json()
        return JsonResponse(data, safe=False)


class TickerMostrarWeek(View):

    def get(self, request):
        tick = "ALSEA.MX"
        #tick = tickerid
        interval = "1wk"
        new_ticker = yf.Ticker(tick)
        hist = new_ticker.history(period="1y",interval=interval)
        data = hist.to_json()
        return JsonResponse(data, safe=False)

#--------------------Tecnichal Analisis ---------------------------------------------------        
class TecnicalAnalisis(View):
    def get(self, request, ticker, flag="0"):
        #Ticker
        tick = yf.Ticker(ticker)
        
        #Download data and reset index
        df = tick.history(period="2mo").reset_index()[[ "Date", "Open","High","Low","Close", "Volume" ]]
        
        #RSI
        df["rsi"] = RSIIndicator(df["Close"], window=14).rsi()
        
        #ADX Indicator
        adx = ADXIndicator(df["High"], df["Low"], df["Close"], window=14)
        df["adx"] = adx.adx() 

        #Stochastic Oscillator
        df["stOscillator"] = StochasticOscillator(df["High"], df["Low"], df["Close"], window=14).stoch()
        
        #Average True Range
        df["AvgTrueRange"] = AverageTrueRange(df["High"], df["Low"], df["Close"]).average_true_range()

        #Grab the last row from Data Frame
        last = df.iloc[-1]
        
        #Convert Pandas Data Frame in JSON format
        if flag == "1":   
            data = last.to_json()
        else:
            data = df.to_json() 

        return JsonResponse(data, safe=False)

#-------------------------------------------------------------------------------------------------
class Comodities(View):
    def get(self, request):
        #Gold, Natural Gas, Silver, Crude Oil, Cocoa v 
        # NG SI CL=F CC=F
        data = yf.download("GC=F NG CL=F CC=F SI", period="1mo",
        group_by="ticker", actions=False, threads=True, rounding=True)
        # new = data.reset_index()[[ "Date", "Open","High","Low","Close", "Volume" ]]
        
        # Separo los datos
        close = data['NG']['Close']
        closeGC = data['GC=F']['Close']
        closeCL = data['CL=F']['Close']
        closeCC = data['CC=F']['Close']
        closeSI = data['SI']['Close']

        #nani = close.append(close2)
        
        # reseteo los indices de los 2 tickers
        new = close.reset_index()[["Date","Close"]]
        new1 = closeGC.reset_index()[["Close"]]
        new2 = closeCL.reset_index()[["Close"]]
        new3 = closeCC.reset_index()[["Close"]]
        new4 = closeSI.reset_index()[["Close"]]
        

        # Les cambio los nombres de Close a Tickername
        new = new.rename(columns={"Close": "NG"})
        new1 = new1.rename(columns={"Close": "GC"})
        new2 = new2.rename(columns={"Close": "CL"})
        new3 = new3.rename(columns={"Close": "CC"})
        new4 = new4.rename(columns={"Close": "SI"})
        # print(new1)
        # append data
        datos = pd.concat([new,new1,new2,new3,new4], axis=1)
        # print(datos)
        
        # data = data.iloc[-1].to_json()
        neww = datos.to_json()
        return JsonResponse(neww, safe=False)
        

class ComoditiesList(View):
    def get(self, request):
        #Gold, Natural Gas, Silver, Crude Oil, Cocoa v 
        # NG SI CL=F CC=F
        data = yf.download("GC=F NG", period="1mo",
        group_by="ticker", actions=False, threads=True, rounding=True)
        # new = data.reset_index()[[ "Date", "Open","High","Low","Close", "Volume" ]]
        print(data['NG']['Close'])
        # data = data.iloc[-1].to_json()

        return JsonResponse(data, safe=False)

class NewsList(View):
    def get(self, request):

        query_params = {
            "source": "the-verge",
            "sortBy": "top",
            "apiKey": "b2e4276e155d4b3e8c7786b250158584"
            }
        main_url = " https://newsapi.org/v1/articles"

        #Fetching data in json format
        #Obtenemos el status
        res = requests.get(main_url, params=query_params)
        #Obtenemos toda la salida del query en Json format NO FILTRADO
        open_bbc_page = res.json()
        # getting all articles in a string article
        article = open_bbc_page["articles"]

        return JsonResponse(article, safe=False)
     


#@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def ticker_list(request, ticker_id): 
    if request.method == 'GET' or  request.method == 'POST':
        tick = ticker_id
        new_ticker = yf.Ticker(tick)
        
        historical = new_ticker.history(period="1mo",interval="1mo")
        data = historical.to_json()
        
        return Response(data)

def stock_list(request,patterMatch = " " ):
    # if request.method == 'GET':
    stocks =  Mex_stocks.objects.all() 
    serializer = Mex_stocks_Serializer(stocks, many=True)
    with connection.cursor() as cursor:
      cursor.execute("SELECT id_name FROM api_basic_mex_stocks WHERE id_name LIKE %s ", [patterMatch + "%"])
    
      row = cursor.fetchall()
      return JsonResponse(row,safe=False)
