import json
import time

import ds18x20
import machine
import onewire


def load_secrets(file_path: str):
    """Load and parse JSON secrets from a file.

    Args:
        file_path (str): Path to the secrets JSON file.

    Returns:
        dict: Parsed JSON content from the secrets file.
    """
    with open(file_path) as secret_file:
        return json.loads(secret_file.read())


def check_connection(wlan, max_retries=200):
    """Check and wait for WiFi connection to be established.

    Args:
        wlan: WiFi network interface object.
        max_retries (int): Maximum number of connection attempts.

    Returns:
        bool: True if connection is successful.

    Raises:
        OSError: If connection fails after maximum retries.
    """
    for _ in range(max_retries):
        if wlan.isconnected():
            print(f'\nConnected. \nNetwork config: {wlan.ifconfig()}')
            time.sleep(1)
            return True
        time.sleep_ms(1000)
        print('.', end='')

    raise OSError(f'Failed to connect to {wlan.config("ssid")}, exceeded max_retries {max_retries}')


def temp_sensor_setup(sensor_pin: int):
    """Initialize and setup DS18X20 temperature sensor.

    Args:
        sensor_pin (int): GPIO pin number where the sensor is connected.

    Returns:
        DS18X20: Configured temperature sensor object.
    """
    one_wire_pin = machine.Pin(sensor_pin)
    one_wire = onewire.OneWire(one_wire_pin)
    return ds18x20.DS18X20(one_wire)


def log_over_mqtt(error):
    """Send error log message over MQTT protocol.

    Args:
        error: Error object or message to be logged.
    """
    response = {"log": {
        "level": 50,
        "message": f"Error: {error}"
    }}
    from main import CLIENT
    from config import TOPIC
    CLIENT.publish(TOPIC, json.dumps(response))
    print(f'System returned error with message: {error}. \nUnit will restart')


def log_and_restart(error):
    """Log error over MQTT and restart the system.

    Args:
        error: Error object or message to be logged before restart.
    """
    log_over_mqtt(error)
    machine.reset()
