from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Ticket

class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'