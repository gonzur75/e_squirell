from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Avg
from django.db.models.functions import TruncHour, TruncDay, TruncMonth

from energy_tracker.models import EnergyLog
from energy_tracker.serializers import EnergyLogSerializer

class EnergyLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnergyLog.objects.all()
    serializer_class = EnergyLogSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        resolution = request.query_params.get('resolution')
        if resolution in ['hourly', 'daily', 'monthly']:
            if resolution == 'hourly':
                trunc_func = TruncHour
            elif resolution == 'daily':
                trunc_func = TruncDay
            else:
                trunc_func = TruncMonth
            
            numeric_fields = [
                f.name for f in EnergyLog._meta.fields 
                if f.name not in ['timestamp', 'id', 'device_status', 'voltage_phase_seq']
            ]
            annotations = {f: Avg(f) for f in numeric_fields}
            
            queryset = self.get_queryset().annotate(
                trunc_ts=trunc_func('timestamp')
            ).values('trunc_ts').annotate(**annotations).order_by('-trunc_ts')
            
            # Reconstruct the response dictionaries to map trunc_ts back to timestamp
            page = self.paginate_queryset(queryset)
            if page is not None:
                results = []
                for item in page:
                    item['timestamp'] = item.pop('trunc_ts')
                    results.append(item)
                return self.get_paginated_response(results)

            results = []
            for item in queryset:
                item['timestamp'] = item.pop('trunc_ts')
                results.append(item)
            return Response(results)

        return super().list(request, *args, **kwargs)
