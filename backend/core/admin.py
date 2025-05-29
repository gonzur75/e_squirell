from pickle import GLOBAL

from django.contrib import admin
from core.models import ProjectSettings


@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ProjectSettings.objects.exists()
