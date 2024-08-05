import json
import time

from config import CLIENT_ID, MQTT_SERVER, TOPIC, MESSAGE_INTERVAL
from heating import get_status
from helpers import restart_and_reconnect
from mqtt import StorageHeaterClient

LAST_MESSAGE = 0



try:
    print('Setting up mqtt connection')
    CLIENT = StorageHeaterClient(CLIENT_ID, MQTT_SERVER, keepalive=60)
    CLIENT.setup(TOPIC)
except OSError as e:
    restart_and_reconnect(e)


def run():
    try:
        if (time.time() - LAST_MESSAGE) > MESSAGE_INTERVAL:
            payload = json.dump(get_status())

            CLIENT.publish(topic=TOPIC, payload=get_status())

        CLIENT.check_msg()
        time.sleep(5)
    except OSError as error:
        restart_and_reconnect(error)
    return


while True:
    run()
