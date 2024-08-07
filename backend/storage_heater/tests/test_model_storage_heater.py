import pytest

from conftest import fake

from storage_heater.models import StorageHeater


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


def test_storage_heater_status_creation(storage_heater_status):
    assert isinstance(storage_heater_status, StorageHeater)
    assert [*vars(storage_heater_status)] == [
        '_state', 'time_stamp', 'relay_one', 'relay_two', 'relay_three', 'relay_four',
        'relay_five', 'relay_six', 'temp_one', 'temp_two', 'temp_three',
        'temp_four']

    for var in vars(storage_heater_status):
        if var.startswith('relay'):
            assert getattr(storage_heater_status, var) in (0, 1)

        if var.startswith('temp'):
            assert isinstance(getattr(storage_heater_status, var), float)
