from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def energy_field(default=0, min_val=0, max_val=2_000_000_000):
    return models.IntegerField(default=default, validators=[MinValueValidator(min_val), MaxValueValidator(max_val)])


class EnergyLog(models.Model):
    MAX_VOLTAGE = 5_000
    MAX_CURRENT = 3_000_000
    MAX_POWER = 600_000
    MAX_ENERGY = 2_000_000_000
    MAX_TOTAL_POWER = 19_800_000

    timestamp = models.DateTimeField(auto_now_add=True)

    voltage_a = energy_field(max_val=MAX_VOLTAGE)
    voltage_b = energy_field(max_val=MAX_VOLTAGE)
    voltage_c = energy_field(max_val=MAX_VOLTAGE)

    current_a = energy_field(max_val=MAX_CURRENT)
    current_b = energy_field(max_val=MAX_CURRENT)
    current_c = energy_field(max_val=MAX_CURRENT)

    active_power_a = energy_field(min_val=-MAX_POWER, max_val=MAX_POWER)
    active_power_b = energy_field(min_val=-MAX_POWER, max_val=MAX_POWER)
    active_power_c = energy_field(min_val=-MAX_POWER, max_val=MAX_POWER)

    reactive_power_a = energy_field(max_val=MAX_POWER)
    reactive_power_b = energy_field(max_val=MAX_POWER)
    reactive_power_c = energy_field(max_val=MAX_POWER)

    energy_consumed_a = energy_field(max_val=MAX_ENERGY)
    energy_consumed_b = energy_field(max_val=MAX_ENERGY)
    energy_consumed_c = energy_field(max_val=MAX_ENERGY)

    reverse_energy_a = energy_field(max_val=MAX_ENERGY)
    reverse_energy_b = energy_field(max_val=MAX_ENERGY)
    reverse_energy_c = energy_field(max_val=MAX_ENERGY)

    power_factor_a = energy_field(max_val=100)
    power_factor_b = energy_field(max_val=100)
    power_factor_c = energy_field(max_val=100)

    total_energy_consumed = energy_field(max_val=MAX_ENERGY)
    total_reverse_energy = energy_field(max_val=MAX_ENERGY)
    total_current = energy_field(max_val=9_000_000)
    total_active_power = energy_field(min_val=-MAX_TOTAL_POWER, max_val=MAX_TOTAL_POWER)
    total_reactive_power = energy_field(max_val=MAX_TOTAL_POWER)
    frequency = energy_field(max_val=80)
    unit_temp = energy_field(min_val=-100, max_val=800)
    device_status = models.SmallIntegerField()
    voltage_phase_seq = models.SmallIntegerField()

    class Meta:
        ordering = ["-timestamp"]
