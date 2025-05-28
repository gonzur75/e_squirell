import json
import time

import ds18x20
import machine
import onewire


def load_secrets(file_path: str):
    with open(file_path) as secret_file:
        return json.loads(secret_file.read())


def check_connection(wlan, max_retries=200):
    for _ in range(max_retries):
        if wlan.isconnected():
            print(f'\nConnected. \nNetwork config: {wlan.ifconfig()}')
            time.sleep(1)
            return True
        time.sleep(1)
        print('.', end='')

    raise OSError(f'Failed to connect to {wlan.config("ssid")}, exceeded max_retries {max_retries}')


def temp_sensor_setup(sensor_pin: int):
    one_wire_pin = machine.Pin(sensor_pin)
    one_wire = onewire.OneWire(one_wire_pin)
    return ds18x20.DS18X20(one_wire)


def log_and_restart(error):
    response = {"log": {
        "level": 50,
        "message": f"Error in heating: {error}"
    }}
    from main import CLIENT
    from config import TOPIC
    CLIENT.publish(TOPIC, json.dumps(response))
    print(f'System returned error with message: {error}. \nUnit will restart')
    time.sleep(5)

    machine.reset()
