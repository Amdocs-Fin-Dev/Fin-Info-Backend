from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Ticket, Mex_stocks

class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class Mex_stocks_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Mex_stocks
        fields = '__all__' 