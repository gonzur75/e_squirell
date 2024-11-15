from rest_framework.routers import SimpleRouter

from . import views

app_name = 'energy_tracker_api'

router = SimpleRouter()
router.register('', views.EnergyLogViewSet, basename='energy_tracker')

urlpatterns = router.urls
