from conftest import storage_heater_status
from storage_heater.models import StorageHeater


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
