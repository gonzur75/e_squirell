from rest_framework import serializers
from storage_heater.models import StorageHeater


class StorageHeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageHeater
        fields = ("time_stamp",
                  "relay_one",
                  "relay_two",
                  "relay_three",
                  "relay_four",
                  "relay_five",
                  "relay_six",
                  "temp_one",
                  "temp_two",
                  "temp_three",
                  "temp_four",)
