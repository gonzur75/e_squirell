from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import ProjectSettings
from .serializers import ProjectSettingsSerializer

class ProjectSettingsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProjectSettings.objects.all()
    serializer_class = ProjectSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # Return the singleton instance
        obj, _ = ProjectSettings.objects.get_or_create(id=1)
        return obj
