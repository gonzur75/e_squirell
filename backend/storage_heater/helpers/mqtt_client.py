import json
import logging

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MqttService:
    def __init__(self, client):
        self.client = client

    def connect(self):

        try:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
            # self.client.on_message = self.on_message
            self.client.on_connect = self.on_connect
            self.client.connect(
                host=settings.MQTT_SERVER,
                port=settings.MQTT_PORT,
                keepalive=settings.MQTT_KEEPALIVE
            )
            logger.info(f"Connected to Mqtt broker at {settings.MQTT_SERVER}")
        except Exception as error:
            logger.info(f"Unable to connect to Mqtt broker {settings.MQTT_SERVER}: error: {error} ")

    def on_connect(self, mqtt_client, user_data, flags, rc):
        if rc == 0:
            try:
                self.client.subscribe(settings.MQTT_TOPIC)
                logger.info(f"Subscribed to Mqtt topic: {settings.MQTT_TOPIC}")
            except Exception as error:
                logger.error(f"Failed to subscribe to Mqtt topic: {settings.MQTT_TOPIC}: error: {error} ")

def on_message(mqtt_client, userdata, msg):
    from storage_heater.serializers import StorageHeaterSerializer
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload['status']:
        serializer = StorageHeaterSerializer(data=json.loads(payload))
        serializer.is_valid()
        serializer.save()
        logger.info(msg.topic + " " + str(msg.payload))

# client.on_message = on_message
# client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
# client.connect(
#     host=settings.MQTT_SERVER,
#     port=settings.MQTT_PORT,
#     keepalive=settings.MQTT_KEEPALIVE
# )
