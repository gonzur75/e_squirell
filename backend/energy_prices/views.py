from django.shortcuts import render
from rest_framework import generics

from . import models, serializers


# Create your views here.
class ListEnergyPrice(generics.ListAPIView):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = serializers.EnergyPriceSerializer


class DetailEnergyPrice(generics.RetrieveAPIView):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = serializers.EnergyPriceSerializer
