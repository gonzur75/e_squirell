import pytest

from conftest import energy_log
from energy_tracker.models import EnergyLog


@pytest.mark.models
def test_energy_log_creation(energy_log):
    assert isinstance(energy_log, EnergyLog)
    assert EnergyLog.objects.count() == 1


@pytest.mark.models
def test_energy_prices_fields(energy_log):
    assert [*vars(energy_log)] == ["_state", "id", "timestamp", "voltage_a", "voltage_b", "voltage_c", "current_a",
                                   "current_b",
                                   "current_c", "active_power_a", "active_power_b", "active_power_c",
                                   "reactive_power_a", "reactive_power_b", "reactive_power_c", "energy_consumed_a",
                                   "energy_consumed_b", "energy_consumed_c", "reverse_energy_a", "reverse_energy_b",
                                   "reverse_energy_c", "power_factor_a", "power_factor_b", "power_factor_c",
                                   "total_energy_consumed", "total_reverse_energy", "total_current",
                                   "total_active_power", "total_reactive_power", "frequency", "unit_temp",
                                   "device_status", "voltage_phase_seq"]
