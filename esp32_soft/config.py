import machine
import ubinascii
from micropython import const

from helpers import load_secrets, temp_sensor_setup

SECRETS = load_secrets('secrets.json')
SSID = SECRETS["wifi_credentials"]['ssid']
PASSWORD = SECRETS["wifi_credentials"]['password']
MQTT_SERVER = SECRETS['mqtt']['server']
# have to be in order to work correctly
RELAYS = ('relay_one', 'relay_two', 'relay_three', 'relay_four', 'relay_five', 'relay_six')
RELAYS_PIN = {'relay_one': 18, 'relay_two': 19, 'relay_three': 21, 'relay_four': 22, 'relay_five': 23, 'relay_six': 25}
TOPIC = b'heat_storage'
TEMPERATURE_SENSOR_PIN = 14
TEMP_SENSOR = temp_sensor_setup(TEMPERATURE_SENSOR_PIN)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

SENSORS = {
    "temp_one": b'(\x00\x1b\x94\x97\x03\x03\x18',
    "temp_two": b'(\xff"\xc70\x17\x032',
    "temp_three": b'(\x8a(\x94\x97\x04\x03\x99',
    "temp_four": b'(\xff\x08\x101\x17\x03['
}
MESSAGE_INTERVAL = const(60)
