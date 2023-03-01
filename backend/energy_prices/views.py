from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import models, serializers
from .serializers import EnergyPriceSerializer


# Create your views here.
class EnergyPriceViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = EnergyPriceSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class DetailEnergyPrice(generics.RetrieveAPIView):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = serializers.EnergyPriceSerializer
