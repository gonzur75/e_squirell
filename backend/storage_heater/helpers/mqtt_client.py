from config import settings
# from storage_heater.serializers import StorageHeaterSerializer

import paho.mqtt.client as mqtt


def on_connect(mqtt_client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    client.subscribe("heat_storage")


def on_message(mqtt_client, userdata, msg):
    # serializer = StorageHeaterSerializer(msg.payload)
    # serializer.save()
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
