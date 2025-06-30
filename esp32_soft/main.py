import gc
import json
import time

from machine import WDT


from config import CLIENT_ID, MESSAGE_INTERVAL, MQTT_SERVER, TOPIC
from heating import get_status
from helpers import log_and_restart
from mqtt import Client

gc.enable()
wdt = WDT(timeout=50000)

try:
    print('Setting up mqtt connection')
    CLIENT = Client(CLIENT_ID, MQTT_SERVER, keepalive=90)
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
        CLIENT.check_and_restore_mqtt()

        time.sleep_ms(1000)
        wdt.feed()


    return inner

run_instance = run()

while True:
    try:
        run_instance()
    except Exception as error:
        log_and_restart(error)

