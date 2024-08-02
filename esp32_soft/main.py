import time

from config import CLIENT_ID, MQTT_SERVER, TOPIC
from helpers.helpers import restart_and_reconnect
from mqtt import StorageHeaterClient

try:
    print('Setting up mqtt connection')
    CLIENT = StorageHeaterClient(CLIENT_ID, MQTT_SERVER, keepalive=60)
    CLIENT.setup(TOPIC)
except OSError as e:
    restart_and_reconnect(e)


def run():
    try:
        CLIENT.check_msg()
        time.sleep(1)
    except OSError as e:
        restart_and_reconnect(e)
    return


while True:
    run()
