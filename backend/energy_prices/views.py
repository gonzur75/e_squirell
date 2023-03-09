from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .models import EnergyPrice
from .serializers import EnergyPriceSerializer


class EnergyPriceViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyPrice.objects.all()
    serializer_class = EnergyPriceSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly]
    @action(detail=False)
    def last_entry(self, request):
        last_entry = EnergyPrice.objects.latest('valid_from')
        print(last_entry)
        serializer = self.get_serializer(last_entry)
        return Response(serializer.data)


# TODO: decide weather you want authentication or not
