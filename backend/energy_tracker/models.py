from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class EnergyLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage_a = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5_000)])
    voltage_b = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5_000)])
    voltage_c = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5_000)])

    current_a = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3_000_000)])
    current_b = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3_000_000)])
    current_c = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3_000_000)])

    active_power_a = models.IntegerField(default=0,
                                         validators=[MinValueValidator(-600_000), MaxValueValidator(600_000)])
    active_power_b = models.IntegerField(default=0,
                                         validators=[MinValueValidator(-600_000), MaxValueValidator(600_000)])
    active_power_c = models.IntegerField(default=0,
                                         validators=[MinValueValidator(-600_000), MaxValueValidator(600_000)])

    reactive_power_a = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(600_000)])
    reactive_power_b = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(600_000)])
    reactive_power_c = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(600_000)])

    energy_consumed_a = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    energy_consumed_b = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    energy_consumed_c = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])

    reverse_energy_a = models.IntegerField(default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    reverse_energy_b = models.IntegerField(default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    reverse_energy_c = models.IntegerField(default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])

    total_energy_consumed = models.IntegerField(default=0,
                                                validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    total_reverse_energy = models.IntegerField(default=0,
                                               validators=[MinValueValidator(0), MaxValueValidator(2_000_000_000)])
    total_current = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9_000_000)])
    total_active_power = models.IntegerField(default=0,
                                             validators=[MinValueValidator(-19_800_000), MaxValueValidator(19_800_000)])
    total_reactive_power = models.IntegerField(default=0,
                                               validators=[MinValueValidator(0), MaxValueValidator(19_800_000)])
    frequency = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(80)])
    unit_temp = models.IntegerField(default=0, validators=[MinValueValidator(-100), MaxValueValidator(80)])
