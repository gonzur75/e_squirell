from rest_framework.routers import SimpleRouter

from . import views

app_name = 'storage_heater_api'

router = SimpleRouter()
router.register('', views.HeatStorageViewSet, basename='heat_storage')

urlpatterns = router.urls