import json
import time

from config import CLIENT_ID, MESSAGE_INTERVAL, MQTT_SERVER, TOPIC
from heating import get_status
from helpers import restart_and_reconnect
from mqtt import StorageHeaterClient

try:
    print('Setting up mqtt connection')
    CLIENT = StorageHeaterClient(CLIENT_ID, MQTT_SERVER, keepalive=60)
    CLIENT.setup(TOPIC)
except OSError as e:
    restart_and_reconnect(e)


def run():
    last_message = 0

    def inner():
        nonlocal last_message
        if (time.time() - last_message) > MESSAGE_INTERVAL:
            payload = json.dumps(get_status())
            CLIENT.publish(TOPIC, payload)
            last_message = time.time()
        CLIENT.check_msg()
        time.sleep(1)

    return inner

run_instance = run()

while True:
    try:
        run_instance()
    except OSError as error:
        restart_and_reconnect(error)
