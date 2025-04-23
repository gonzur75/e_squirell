import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

import tinytuya
from django.utils import timezone

from energy_tracker.serializers import EnergyLogSerializer


# TODO: Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)


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
                # logger.error(f"Failed to get device status: {status}")
                return None
        except Exception as e:
            # logger.exception(f"Error getting device status: {e}")
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
            # logger.error("Invalid status data format")
            return processed_data

        dps = status['dps']
        map_file: Path = Path(os.getcwd() + "/energy_tracker/mapped_keys.json")

        with open(map_file, 'r') as file:
            dps_map = json.load(file)

        # Log what we got from the device to help with debugging
        # logger.info(f"Received DPS: {dps}")

        for dps_key, model_field in dps_map.items():
            if dps_key in dps and dps[dps_key] is not None:
                value = dps[dps_key]

                processed_data[model_field] = value

        return processed_data

    @staticmethod
    def save_reading_to_db(data: Dict[str, Any]) -> None:
        """
        Save the processed data to the Django model.
        Args:
            data: Processed data dictionary with readings
        """

        try:
            serializer = EnergyLogSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        except Exception as e:
            print(e)

    # logger.exception(f"Failed to save reading to database: {e}")

    def fetch_and_save(self) -> bool:
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
            if processed_data:
                self.save_reading_to_db(processed_data)
                return True
            else:
                # logger.warning("No data was processed from device status")
                return False
        except Exception as e:
            # logger.exception(f"Error in fetch_and_save: {e}")
            return False
