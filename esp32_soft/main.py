import gc
import json
import time

from config import CLIENT_ID, MESSAGE_INTERVAL, MQTT_SERVER, TOPIC
from heating import get_status
from helpers import log_and_restart
from mqtt import StorageHeaterClient

try:
    print('Setting up mqtt connection')
    CLIENT = StorageHeaterClient(CLIENT_ID, MQTT_SERVER, keepalive=60)
    CLIENT.setup(TOPIC)
except OSError as error:
    log_and_restart(error)


def run():
    last_message = 0

    def inner():
        nonlocal last_message
        now = time.time()
        if (now - last_message) > MESSAGE_INTERVAL:
            payload = json.dumps(get_status())
            CLIENT.publish(TOPIC, payload)
            last_message = now
            gc.collect()
        CLIENT.check_msg()
        time.sleep(1)


    return inner

run_instance = run()

while True:
    try:
        run_instance()
    except OSError as error:
        log_and_restart(error)
