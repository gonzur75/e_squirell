from rest_framework import generics, viewsets

from . import models, serializers
from .serializers import EnergyPriceSerializer


class EnergyPriceViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = EnergyPriceSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

