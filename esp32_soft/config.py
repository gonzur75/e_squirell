import machine
import ubinascii
from micropython import const

from helpers import load_secrets, temp_sensor_setup

SECRETS = load_secrets('secrets.json')
SSID = SECRETS["wifi_credentials"]['ssid']
PASSWORD = SECRETS["wifi_credentials"]['password']
MQTT_SERVER = SECRETS['mqtt']['server']
RELAYS_PIN = {'relay_one': 18, 'relay_two': 19, 'relay_three': 21, 'relay_four': 22, 'relay_five': 23, 'relay_six': 25}
TOPIC = b'heat_storage'
TEMPERATURE_SENSOR_PIN = 14
TEMP_SENSOR = temp_sensor_setup(TEMPERATURE_SENSOR_PIN)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

SENSORS = {"temp_one": b'(\xff"\xc70\x17\x032'}
MESSAGE_INTERVAL = const(60)
