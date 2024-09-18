import json

from config import settings
from paho.mqtt.client import MQTTMessage


def mqtt_message_for_testing(data):
    payload = json.dumps(data)
    msg = MQTTMessage(settings.MQTT_TOPIC)
    msg.payload = payload.encode('utf-8')
    return msg
