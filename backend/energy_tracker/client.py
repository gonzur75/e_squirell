import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

import pytz
import tinytuya
from django.conf import settings

from energy_tracker.serializers import EnergyLogSerializer
import paho.mqtt.publish as publish

from storage_heater.models import StorageHeater

logger = logging.getLogger(__name__)

HEATING_REQUIRED = False


class PC321MeterClient:
    """Client to interact with Tuya Smart Meter devices using tinytuya and save data to Django."""

    def __init__(self, device_id: str, device_ip: str, local_key: str, device_version: float = 3.3):
        """
        Initialize the TinyTuya client.

        Args:
            device_id: ID of the Tuya smart meter device
            device_ip: IP address of the device on the local network
            local_key: Local key for device communication
            device_version: Protocol version (default 3.3)
        """
        self.device = tinytuya.Device(
            dev_id=device_id,
            address=device_ip,
            local_key=local_key,
            version=device_version
        )

    def get_device_status(self) -> Optional[Dict[str, Any]]:
        """Get the current status of the device."""
        try:
            self.device.set_socketTimeout(5)
            status = self.device.status()
            if status and 'dps' in status:
                return status
            else:
                logger.error(f"Failed to get device status: {status}")
                return None
        except Exception as e:
            logger.exception(f"Error getting device status: {e}")
            return None

    @staticmethod
    def process_device_data(status: Dict[str, Any]) -> Dict[str, float]:
        """
        Process the raw data from the device into a normalized format.
        Args: status: Status data from the device
        Returns: Dictionary with normalized readings
        """
        processed_data = {}

        if not status or 'dps' not in status:
            logger.error("Invalid status data format")
            return processed_data

        dps = status['dps']
        map_file: Path = Path(os.getcwd() + "/energy_tracker/mapped_keys.json")

        with open(map_file, 'r') as file:
            dps_map = json.load(file)

        for dps_key, model_field in dps_map.items():
            if dps_key in dps and dps[dps_key] is not None:
                value = dps[dps_key]

                processed_data[model_field] = value

        return processed_data

    @staticmethod
    def save_reading_to_db(data: Dict[str, Any]) -> Union[dict, None]:
        """
        Save the processed data to the Django model.
        Args:
            data: Processed data dictionary with readings
        """

        try:
            serializer = EnergyLogSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return serializer.validated_data
            return None

        except Exception as e:
            print(e)

    # logger.exception(f"Failed to save reading to database: {e}")

    def fetch_and_process_data(self) -> bool:
        """
        Fetch data from the Tuya device and save it to the database.

        Returns:
            Boolean indicating success or failure
        """
        try:
            status_data = self.get_device_status()
            if not status_data:
                return False

            processed_data = self.process_device_data(status_data)
            if processed_data and (validated_data := self.save_reading_to_db(processed_data)):
                process_smart_meter_data(validated_data)
                return True
            else:
                logger.warning("No data was processed from device status")
                return False
        except Exception as e:
            logger.exception(f"Error in fetch_and_save: {e}")
            return False


RELAYS_MAP = {
    "a": 2,
    "b": 1,
    "c": 3,
}


def process_smart_meter_data(data: dict):
    active_power = data["total_active_power"]
    voltage_threshold = 24950
    safe_voltage_threshold = 2460
    # [('voltage_a', 2134),  ...]
    voltage_per_phase = sorted((x for x in data.items() if x[0] in ('voltage_a', 'voltage_b', 'voltage_c')),
                               key=lambda x: x[1], reverse=True)
    if HEATING_REQUIRED:

        if active_power > 2400:
            for phase_name, _ in voltage_per_phase[:3]:
                relay_number = get_relay_number(phase_name)
                send_relay_action(relay_number, 'on')
            return None
        elif active_power > 1600:
            for phase_name, _ in voltage_per_phase[:2]:
                relay_number = get_relay_number(phase_name)
                send_relay_action(relay_number, 'on')
            phase_name, _ = voltage_per_phase[2]
            relay_number = get_relay_number(phase_name)
            send_relay_action(relay_number, 'off')
            return None
        elif active_power > 800:
            for phase_name, _ in voltage_per_phase[1:]:
                relay_number = get_relay_number(phase_name)
                send_relay_action(relay_number, 'off')
            phase_name, _ = voltage_per_phase[0]
            relay_number = get_relay_number(phase_name)
            send_relay_action(relay_number, 'on')
            return None
        else:
            for phase_name, _ in voltage_per_phase:
                relay_number = get_relay_number(phase_name)
                send_relay_action(relay_number, 'off')
            return None

    elif 10 <= datetime.now(pytz.timezone('Europe/Warsaw')).hour < 17:
        # stabilising voltage in case of high energy production in sumer when heating is not required
        # but it could be used for droping excesiv voltage that coses falownik to switchoff
        relays: list[str] = [x.name for x in StorageHeater._meta.get_fields() if x.name.startswith('relay_')]
        storage_heater_relays = StorageHeater.objects.values(*relays).first()
        one_kw_heaters_on = {k: v for k, v in list(storage_heater_relays.items())[:3] if v is True}
        two_kw_heaters_on = {k: v for k, v in list(storage_heater_relays.items())[3:] if v is True}

        phases_with_voltage_over_threshold = [x for x in voltage_per_phase if x[1] > voltage_threshold]
        phases_with_voltage_under_safe_threshold = all([x for x in voltage_per_phase if x[1] < safe_voltage_threshold])

        if phases_with_voltage_over_threshold:
            if one_kw_heaters_on and not two_kw_heaters_on:
                match_one_kw_heaters_with_overvoltage_phases = []
                for heater in one_kw_heaters_on:
                    for phase, _ in phases_with_voltage_over_threshold:
                        phase_number = get_relay_number(phase)
                        if f"relay_{phase_number}" in heater:
                            match_one_kw_heaters_with_overvoltage_phases.append(phase_number)
                            break
                if len(match_one_kw_heaters_with_overvoltage_phases) == 1:
                    phase_number = match_one_kw_heaters_with_overvoltage_phases[0]
                    send_relay_action(phase_number + 3, 'on')
                    send_relay_action(phase_number, 'off')
                    return None

                elif not match_one_kw_heaters_with_overvoltage_phases:
                    for phase, voltage in phases_with_voltage_over_threshold:
                        relay_number = get_relay_number(phase)
                        send_relay_action(relay_number, 'on')
                        return None
                    return None

                elif len(match_one_kw_heaters_with_overvoltage_phases) > 1:
                    turn_off_relays(voltage_per_phase)
                    return None
                return None

            elif one_kw_heaters_on and two_kw_heaters_on:
                turn_off_relays(voltage_per_phase)
                return None

            else:
                for phase, voltage in phases_with_voltage_over_threshold:
                    relay_number = get_relay_number(phase)
                    send_relay_action(relay_number, 'on')
                    return None
                return None

        elif phases_with_voltage_under_safe_threshold:
            turn_off_relays(voltage_per_phase)
            return None
        return None
    return None


def send_relay_action(relay_number, relay_action="on"):
    payload = {"heating_action": f'relay_{relay_number}_{relay_action}'}
    publish.single(settings.MQTT_TOPIC, json.dumps(payload), hostname=settings.MQTT_SERVER)


def get_relay_number(phase_name):
    return RELAYS_MAP[phase_name[-1]]

def turn_off_relays(phases):
    for phase, _ in phases:
        send_relay_action(get_relay_number(phase), 'off')
