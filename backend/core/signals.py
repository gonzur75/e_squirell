from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ProjectSettings


@receiver([post_save], sender=ProjectSettings)
def invalidate_project_settings_cache(sender, **kwargs):
    cache.delete("project_settings")