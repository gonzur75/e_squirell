from rest_framework import serializers

from energy_prices import models


class EnergyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnergyPrice
        fields = (
            'value_inc_vat',
            'valid_to',
            'valid_from',
        )
