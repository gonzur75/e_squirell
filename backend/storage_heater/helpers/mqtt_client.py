import json

from config import settings


import paho.mqtt.client as mqtt


def on_connect(mqtt_client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    client.subscribe(settings.MQTT_TOPIC)


def on_message(mqtt_client, userdata, msg):
    from storage_heater.serializers import StorageHeaterSerializer
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload['status']:
        serializer = StorageHeaterSerializer(data=json.loads(payload))
        serializer.is_valid()
        serializer.save()
        print(msg.topic + " " + str(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
