from core.models import ProjectSettings


def get_project_settings():
    from django.core.cache import cache
    from django.conf import settings

    cache_key = 'project_settings'
    cached_settings = cache.get(cache_key)

    if cached_settings is None:
        cached_settings = ProjectSettings.objects.first()
        cache.set(cache_key, cached_settings)

    return cached_settings
