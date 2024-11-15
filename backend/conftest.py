from unittest.mock import patch

import pytest
from _decimal import Decimal
from energy_prices.models import EnergyPrice
from faker import Faker
from rest_framework.test import APIRequestFactory

from energy_tracker.models import EnergyLog
from storage_heater import MqttService
from storage_heater.models import StorageHeater

fake = Faker()

@pytest.fixture
def api_request_factory():
    return APIRequestFactory()

@pytest.fixture
def energy_price(db):
    return EnergyPrice.objects.create(
        value_inc_vat=Decimal(fake.bothify(text='##.##')),
        valid_to=fake.date_time_this_month(),
        valid_from=fake.date_time_this_month(),
    )


@pytest.fixture
def storage_heater_status(db):
    yield StorageHeater.objects.create(
        relay_one=fake.random_int(min=0, max=1),
        relay_two=fake.random_int(min=0, max=1),
        relay_three=fake.random_int(min=0, max=1),
        relay_four=fake.random_int(min=0, max=1),
        relay_five=fake.random_int(min=0, max=1),
        relay_six=fake.random_int(min=0, max=1),
        temp_one=fake.pyfloat(left_digits=3, right_digits=1, min_value=-55, max_value=120),
        temp_two=fake.pyfloat(left_digits=3, right_digits=1, min_value=-55, max_value=120),
        temp_three=fake.pyfloat(left_digits=3, right_digits=1, min_value=-55, max_value=120),
        temp_four=fake.pyfloat(left_digits=3, right_digits=1, min_value=-55, max_value=120),
    )


@pytest.fixture
def mock_client():
    with patch('paho.mqtt.client.Client') as mock_client:
        yield mock_client


@pytest.fixture
def service(mock_client):
    return MqttService(mock_client)


@pytest.fixture
def energy_log(db):
    return EnergyLog.objects.create(voltage_a=230, voltage_b=233, voltage_c=234, current_a=5000)
