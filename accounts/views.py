import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators import csrf
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from yfinance import ticker 
from .models import Account, Portfolio, PortfolioManager
from .serializers import AccountSerializer, PortfolioSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.

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

    
