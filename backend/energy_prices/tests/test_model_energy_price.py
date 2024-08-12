import datetime
from decimal import Decimal

import pytest
from energy_prices.models import EnergyPrice


@pytest.mark.models
def test_energy_prices_creation(energy_price):

    assert isinstance(energy_price, EnergyPrice)
    assert isinstance(energy_price.value_inc_vat, Decimal)
    assert isinstance(energy_price.valid_to, datetime.datetime)
    assert isinstance(energy_price.valid_from, datetime.datetime)


@pytest.mark.models
def test_energy_prices_fields(energy_price):
    assert [*vars(energy_price)] == ['_state', 'id', 'valid_from', 'valid_to', 'value_inc_vat']
