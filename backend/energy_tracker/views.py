from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from energy_tracker.models import EnergyLog
from energy_tracker.serializers import EnergyLogSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EnergyLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnergyLog.objects.all()
    serializer_class = EnergyLogSerializer
    pagination_class = StandardResultsSetPagination
