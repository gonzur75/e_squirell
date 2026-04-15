from rest_framework.routers import SimpleRouter
from . import views

app_name = 'core_api'

router = SimpleRouter()
router.register('settings', views.ProjectSettingsViewSet, basename='project_settings')

urlpatterns = router.urls
