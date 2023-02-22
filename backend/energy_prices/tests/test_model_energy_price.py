from decimal import Decimal

import datetime
import pytest

from faker import Faker

from energy_prices.models import EnergyPrice

fake = Faker()

@pytest.fixture
def energy_price(db):
    return EnergyPrice.objects.create(
        value_inc_vat=Decimal(fake.bothify(text='##.##')),
        valid_to=fake.date_time_this_month(),
        valid_from=fake.date_time_this_month(),
    )


@pytest.mark.models
def test_energy_prices_creation(energy_price):

    assert isinstance(energy_price, EnergyPrice)
    assert isinstance(energy_price.value_inc_vat, Decimal)
    assert isinstance(energy_price.valid_to, datetime.datetime)
    assert isinstance(energy_price.valid_from, datetime.datetime)


@pytest.mark.models
def test_energy_prices_fields(energy_price):
    assert [*vars(energy_price)] == ['_state', 'valid_from', 'valid_to', 'value_inc_vat']
