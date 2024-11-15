
from rest_framework import viewsets

from energy_tracker.models import EnergyLog
from energy_tracker.serializers import EnergyLogSerializer


class EnergyLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnergyLog.objects.all()
    serializer_class = EnergyLogSerializer
