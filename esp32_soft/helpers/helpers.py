import json
import time

import ds18x20
import machine
import network
import onewire


def load_secrets(file_path: str):
    with open(file_path) as secret_file:
        return json.loads(secret_file.read())


def wlan_connect(ssid, password, max_retries=200):
    wlan = network.WLAN(network.STA_IF)

    print(f'Connecting to network: {ssid}.')
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(max_retries):
        if wlan.isconnected():
            print(f'\nConnected. \nNetwork config: {wlan.ifconfig()}')
            time.sleep(1)
            return True
        time.sleep(0.1)
        print('.', end='')

    print(f'Failed to connect to {ssid}')


def temp_sensor_setup(sensor_pin: int):
    one_wire_pin = machine.Pin(sensor_pin)
    one_wire = onewire.OneWire(one_wire_pin)
    return ds18x20.DS18X20(one_wire)


def restart_and_reconnect(error):
    print(f'System returned error with message: {error}. \nUnit will restart')
    time.sleep(5)
    machine.reset()
