from datetime import date, timezone
import datetime
from time import time
from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Account(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    idToken = models.CharField(max_length=1500)

    def __str__(self):
        return self.email


class PortfolioManager(models.Manager):
    def get_queryset(self, email='', ticker=''):
        return super(PortfolioManager,self).get_queryset().filter(email=email)

    def create(self,**kwargs):
        return super().create(**kwargs)

    # def delete(self, ticker):
    #     return super().delete()

    # def get_queryset2(self, email='', ticker=''):
    #     return super(PortfolioManager, self).get_queryset().filter(email=email, ticker=ticker)

class Portfolio(models.Model):
    email = models.EmailField(max_length=50)
    ticker = models.CharField(max_length=50)

    objects = PortfolioManager()

    def __str__(self):
        return self.email


class InvestManager(models.Manager):
    def get_queryset(self, email=''):
        return super(InvestManager,self).get_queryset().filter(email=email)

    def create(self,**kwargs):
        return super().create(**kwargs)

class Invest(models.Model):
    email = models.EmailField(max_length=100)
    tickerTrade = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    dateInvest = models.DateField(default=date.today)

    objects = InvestManager()

    def __str__(self) -> str:
        return self.email