from rest_framework import serializers

from energy_tracker.models import EnergyLog


class EnergyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyLog
        fields = ("timestamp",
                  "voltage_a",
                  "voltage_b",
                  "voltage_c",
                  "current_a",
                  "current_b",
                  "current_c",
                  "active_power_a",
                  "active_power_b",
                  "active_power_c",
                  "reactive_power_a",
                  "reactive_power_b",
                  "reactive_power_c",
                  "energy_consumed_a",
                  "energy_consumed_b",
                  "energy_consumed_c",
                  "reverse_energy_a",
                  "reverse_energy_b",
                  "reverse_energy_c",
                  "total_energy_consumed",
                  "total_reverse_energy",
                  "total_current",
                  "total_active_power",
                  "total_reactive_power",
                  "frequency",
                  "unit_temp"
                  )
