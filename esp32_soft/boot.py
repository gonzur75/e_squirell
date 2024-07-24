
import time
import ubinascii
import machine
import network
import esp

esp.osdebug(None)
import gc

gc.collect()

mqtt_server = "192.168.8.2"  # 'REPLACE_WITH_YOUR_MQTT_BROKER_IP'
# EXAMPLE IP ADDRESS
# mqtt_server = '172.17.0.1'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

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

# station = network.WLAN(network.STA_IF)
#
# station.active(True)
# station.connect(ssid, password)
#
# while station.isconnected() == False:
#   print('disconnected')
#
# print('Connection successful')
# print(station.ifconfig())
