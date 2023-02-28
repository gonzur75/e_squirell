import pytest
from django.urls import reverse

from energy_prices.models import EnergyPrice


def test_energy_price_listview(client, energy_price):
    endpoint = reverse("energy_price_api:energy_price_list")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert str(energy_price.value_inc_vat) in response.content.decode('utf-8')
    assert EnergyPrice.objects.count() == 1


def test_energy_price_detail_view(client, energy_price):
    endpoint = reverse("energy_price_api:energy_price_detail", kwargs={"pk": energy_price.id})
    response = client.get(endpoint, format="json")

    assert response.status_code == 200
    assert str(energy_price.value_inc_vat) in response.content.decode('utf-8')
