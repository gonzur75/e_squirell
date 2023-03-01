from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'energy_price_api'

router = SimpleRouter()
router.register('energy_prices', views.EnergyPriceViewSet, basename='energy_prices')

urlpatterns = router.urls
# urlpatterns = [
#
#     # path('', views.ListEnergyPrice.as_view(), name="energy_price_list"),
#     # path('<int:pk>/', views.DetailEnergyPrice.as_view(), name="energy_price_detail"),
# ]
