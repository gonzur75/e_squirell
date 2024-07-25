import time

import machine
import network
import esp
import onewire
import ds18x20
esp.osdebug(None)
import gc

gc.collect()

SSID = 'Strugalowka'
PASSWORD = 'Akacja17'


def wlan_connect(ssid, password, max_retries=200):
    wlan = network.WLAN(network.STA_IF)

    print(f'Connecting to network: {ssid}.')
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(max_retries):
        if wlan.isconnected():
            print(f'\nConnected. \nNetwork config: {wlan.ifconfig()}')
            return True
        time.sleep(0.1)
        print('.', end='')

    print(f'Failed to connect to {ssid}')


def temp_sensor_setup():
    one_wire_pin = machine.Pin(14)
    one_wire = onewire.OneWire(one_wire_pin)
    return ds18x20.DS18X20(one_wire)


try:
    wlan_connect(SSID, PASSWORD)
    TEMP_SENSOR = temp_sensor_setup()
except OSError as error:
    print(f'System returned error with message: {error}. \nPlease restart your device ')
