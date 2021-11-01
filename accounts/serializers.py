from django.db import models
from rest_framework import fields, serializers
from .models import Account, Invest, Portfolio

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class InvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invest
        fields = '__all__'