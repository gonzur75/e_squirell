from energy_prices.views import EnergyPriceViewSet


def test_energy_price_listview(db, api_request_factory, energy_price):
    url = "heat_storage_api/v1/energy_prices"
    view = EnergyPriceViewSet.as_view({"get": "list"})

    request = api_request_factory.get(url)
    response = view(request)

    assert response.status_code == 200
