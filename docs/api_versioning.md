# API Versioning Strategy

This document outlines the API versioning strategy used in the E-Squirell project.

## Current Implementation

The E-Squirell API uses URL path versioning to ensure backward compatibility as the API evolves. The versioning strategy follows these principles:

1. All API endpoints are accessible through a unified API structure with a common prefix: `/api/v1/`
2. Legacy endpoints are maintained for backward compatibility

## API Endpoints

### New Unified API Structure (Recommended)

All API endpoints are accessible through the following URL structure:

- `/api/v1/energy_prices/` - Energy prices API
- `/api/v1/storage_heater/` - Storage heater API
- `/api/v1/energy_tracker/` - Energy tracker API

### Legacy Endpoints (Maintained for Backward Compatibility)

The following legacy endpoints are maintained for backward compatibility:

- `/energy_price_api/v1/` - Energy prices API
- `/heat_storage_api/v1/` - Storage heater API
- `/energy_tracker_api/v1/` - Energy tracker API

## Future Versioning

When introducing breaking changes to the API, a new version should be created:

1. Create a new version in the URL structure: `/api/v2/`
2. Maintain the previous version for backward compatibility
3. Document the changes between versions

Example of future versioning:

```python
# API versioning patterns
api_v1_patterns = [
    path('energy_prices/', include('energy_prices.urls')),
    path('storage_heater/', include('storage_heater.urls')),
    path('energy_tracker/', include('energy_tracker.urls')),
]

api_v2_patterns = [
    path('energy_prices/', include('energy_prices.urls_v2')),
    path('storage_heater/', include('storage_heater.urls_v2')),
    path('energy_tracker/', include('energy_tracker.urls_v2')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # API versions
    path('api/v1/', include(api_v1_patterns)),
    path('api/v2/', include(api_v2_patterns)),
    
    # Legacy endpoints for backward compatibility
    path('energy_price_api/v1/', include('energy_prices.urls')),
    path('heat_storage_api/v1/', include('storage_heater.urls')),
    path('energy_tracker_api/v1/', include('energy_tracker.urls'))
]
```

## Best Practices

1. Always maintain backward compatibility for at least one version cycle
2. Document all API changes between versions
3. Encourage clients to migrate to the latest version
4. Consider deprecation notices for endpoints that will be removed in future versions