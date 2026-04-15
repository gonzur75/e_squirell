from rest_framework import serializers
from .models import ProjectSettings

class ProjectSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSettings
        fields = '__all__'
