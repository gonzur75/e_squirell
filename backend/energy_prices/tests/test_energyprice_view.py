from django.urls import reverse

from energy_prices.models import EnergyPrice


def test_energy_price_listview(client, energy_price):
    endpoint = reverse("energy_price_api:energy_price")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert str(energy_price) in response.decode('utf-8')
    assert EnergyPrice.objects.count() == 1

