import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators import csrf
from numpy.lib.index_tricks import AxisConcatenator
import pandas as pd
from requests.sessions import merge_cookies
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from yfinance import ticker 
from .models import Account, Invest, Portfolio, PortfolioManager
from .serializers import AccountSerializer, InvestSerializer, PortfolioSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


import yfinance as yf
import pandas_datareader as pdr
from yfinance import ticker
from datetime import datetime
import numpy as np
# Create your views here.
from IPython.display import display

@csrf_exempt
def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AccountSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def account_detail(request, email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # many is for multiple data
        serializer = AccountSerializer(account)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AccountSerializer(account,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return  JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        account.delete()
        return HttpResponse(status=204)

# -----------------------------------------------------------------

@csrf_exempt
def portfolio_list(request, email, ticker=''):
    if request.method == 'GET':
        #email ="kurohime@gmail.com"
        #aqui iba
        portfolios = Portfolio.objects.get_queryset(email)
        print(portfolios)
        serializer = PortfolioSerializer(portfolios, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    # en este!!
    elif request.method == 'DELETE':
        # portfolio = PortfolioManager.get_queryset2(email=email, ticker=ticker)
        # print("Datos bonitos: ", portfolio)
        print(ticker)
        # portfolio = Portfolio.objects.get(email=email, ticker=ticker)
        # portfolio.delete()
        portfolio = Portfolio.objects.raw('DELETE FROM Portfolio WHERE ticker= %s AND email= %s', [ticker, email])
        print("Muestra algo plis",portfolio)
        print(ticker, email)
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM accounts_portfolio WHERE ticker= %s AND email= %s', [ticker, email])
            # row = cursor.fetchone()
        return JsonResponse("Delete complete!!", safe=False)
        # return row

@csrf_exempt
def portfolio_detail(request, email, ticker):
    try:
        #aqui iba some
        portfolio = Portfolio.objects.get_queryset(email)
        print("aaaaa",portfolio)
        # port = Portfolio.some.get_queryset(email)
    except Portfolio.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # many is for multiple data
        serializer = PortfolioSerializer(portfolio)
        print("Mis datos del portfolio",serializer.data)
        return JsonResponse(serializer.data, safe=False, many=True)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PortfolioSerializer(portfolio,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return  JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # portfolio = Portfolio.some.get_queryset(email)
        # portfolio.delete(ticker)
        # portfolio = Portfolio.some.filter(ticker=ticker, email= email).delete()
        # portfolio = Portfolio.some.get(ticker=ticker)
        print("Muestra algo plis",portfolio)
        portfolio = Portfolio.some.raw('DELETE * WHERE ticker= %s', ticker)
        return HttpResponse(status=204)

#-------------------------------------------------------------
@csrf_exempt
def portifolio_add(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PortfolioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    # elif request.method == 'DELETE':

@csrf_exempt
def invest_add(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InvestSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)

        return JsonResponse(serializer.errors, status= 400)


# @csrf_exempt
# def invest_list(request, email):
#     # if request.method == 'GET':
#         #email ="kurohime@gmail.com"
#         #aqui iba
#     invests = Invest.objects.get_queryset(email)
#     print("Mis inversiones :3",invests)
#     serializer = InvestSerializer(invests, many=True)
#     return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def invest_list(request, email, tickerTrade):
    if request.method == 'GET':
        #Ticker
        tick = yf.Ticker(tickerTrade)
        
        #Download data and reset index
        df = tick.history(period="2mo").reset_index()[["Date", "Open","High","Low","Close", "Volume" ]]
        # print("some plis")
        react = df['Close']
        # df['New'] = 0
        df = df.assign(Percentage = df['Close'] - df['Close'].iloc[-1])
        # df = df.assign(Percentage = 0)

        # print(df)

        col = df["Close"]
        data = list(col)
        diff = []
        # print("Rango de data: ", len(data))
        for i in range(len(data)):
            if i == 0:
                diff.append(0)
            elif i + 1 < len(data):
                some = ((data[i] - data[i + 1]) * 100)/data[i]
                diff.append(some)
                # print(i , some)
            else:
                some = ((data[i] - data[i - 1]) * 100)/data[i]
                diff.append(some)
        # print(diff)
        df = df.assign(Nani= diff)
        

        # print(df)
        invests = Invest.objects.get_queryset(email, tickerTrade)
        # print("Mis inversiones :3",invests)
        
        serializer = InvestSerializer(invests, many=True)
        # df = df.assign(Invests = serializer.data)

        pandita = pd.DataFrame(serializer.data)

        # print(pandita)
        
        #cambiamos el nombre a Date para poder hacer merge 
        pandita = pandita.rename(columns={"dateInvest": "Date"})

        # al dataframe que jalamos, le ponemos el formato de datetime64
        pandita["Date"] = pd.to_datetime(pandita["Date"])
        
        # print("Pandita", pandita["Date"])
        
        # print("Panda", df["Date"])

        # Cambiar la columna de Yahoo para hacer el merge con el otro dataframe
        # df = df.rename(columns={"Date":"dateInvest"})
        # df["Date"] = pd.to_datetime(df["Date"])
        # print(df)
        
        # df = df.assign(amount=0)
        # print(df)

        df.set_index('Date',inplace=True)
        pandita.set_index('Date',inplace=True)

        # df = df.add(pandita)
        
        # print(df)
        # print(pandita)

        # df = df.merge(pandita[["amount"]])
        # df = df.sum(pandita[["amount"]])
        # pandita = pandita.merge(df[["Date","amount"]])
        pandita2 = pd.concat([df, pandita],axis=1)

        # print(pandita)
        # df = pd.concat([df, pandita], axis=0)

        # print(pandita2)
        meruko = pandita2[['Close','Nani', 'amount']].copy()
        meruko = pandita2[['Close','Nani', 'amount']].fillna(0)

        meruko = meruko.assign(final=0)

        print(meruko)

        # print(meruko)
        # meruko["amount"].fillna(0)
        porcentaje = meruko["Nani"]
        monto = meruko["amount"]
        final = meruko["final"]
        dataPorcentaje = list(porcentaje)
        dataMonto = list(monto)
        ganancias = list(final)
        for i in range(len(meruko)):
            if dataMonto[i] > 0:
                # i - 1
                for j in range(i, len(meruko)):
                    temp = (dataMonto[i] * dataPorcentaje[j])/100 
                    ganancias[j] = ganancias[j] + temp + dataMonto[i]

        meruko["final"] = ganancias

        # print("Len de Meruko", len(meruko))
        # for i in range(len(ganancias)):

        #     print(i,ganancias[i])

        # print(meruko)
        data = meruko.reset_index()[["Date", "Close","Nani","amount","final"]]

        print(data)

        data = data.to_json()
 
        return JsonResponse(data, safe=False)

