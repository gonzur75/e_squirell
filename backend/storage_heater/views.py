from rest_framework import viewsets
from storage_heater.models import StorageHeater
from storage_heater.serializers import StorageHeaterSerializer


# Create your views here.
class HeatStorageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StorageHeater.objects.all()
    serializer_class = StorageHeaterSerializer
