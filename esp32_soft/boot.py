import time

import machine
import network
import esp

esp.osdebug(None)
import gc

gc.collect()



last_message = 0
message_interval = 5
counter = 0
SSID = 'Strugalowka'
PASSWORD = 'Akacja17'


def wlan_connect(ssid, password, max_retries=200):
    wlan = network.WLAN(network.STA_IF)
    try:
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

    except OSError as error:
        print(f'System returned error with message:{error}. \nPlease restart your device ')


wlan_connect(SSID, PASSWORD)
