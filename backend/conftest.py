from _decimal import Decimal
from energy_prices.models import EnergyPrice
import pytest

from faker import Faker


@pytest.fixture
def energy_price(db):
    return EnergyPrice.objects.create(
        value_inc_vat=Decimal(fake.bothify(text='##.##')),
        valid_to=fake.date_time_this_month(),
        valid_from=fake.date_time_this_month(),
    )


fake = Faker()
