import esp
import gc

from helpers import load_secrets, wlan_connect, temp_sensor_setup

esp.osdebug(None)
gc.collect()

SECRETS = load_secrets('secrets.json')
SSID = SECRETS["wifi_credentials"]['ssid']
PASSWORD = SECRETS["wifi_credentials"]['password']
RELAYS_PIN = (18, 19, 21, 22, 23, 25)
TEMPERATURE_SENSOR_PIN = 14

try:
    wlan_connect(SSID, PASSWORD)
    TEMP_SENSOR = temp_sensor_setup(TEMPERATURE_SENSOR_PIN)
except OSError as error:
    print(f'System returned error with message: {error}. \nPlease restart your device ')
