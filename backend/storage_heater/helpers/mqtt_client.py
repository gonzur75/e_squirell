import json
import logging

from config import settings

from rest_framework.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MqttService:
    """
       A service class to handle MQTT client operations such as connecting to the broker,
       subscribing to topics, and processing incoming messages.
       """

    def __init__(self, client):
        """
               Initialize the MqttService with an MQTT client.

               :param client: The MQTT client instance.
               """
        self.client = client

    def connect(self):
        """
              Connect to the MQTT broker using the provided client credentials and settings.
              Sets up the on_message and on_connect callbacks.
              Logs the connection status.
              """
        try:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
            self.client.on_message = self.on_message
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
        """
               Callback function that is called when the client connects to the broker.

               :param mqtt_client: The MQTT client instance.
               :param user_data: The private user data as set in Client() or userdata_set().
               :param flags: Response flags sent by the broker.
               :param rc: The connection result.
               """
        if rc == 0:
            try:
                self.client.subscribe(settings.MQTT_TOPIC)
                logger.info(f"Subscribed to Mqtt topic: {settings.MQTT_TOPIC}")
            except Exception as error:
                logger.error(f"Failed to subscribe to Mqtt topic: {settings.MQTT_TOPIC}: error: {error} ")

    def on_message(self, mqtt_client, userdata, msg):

        """
       Callback function that is called when a message is received from the broker.

       :param mqtt_client: The MQTT client instance.
       :param userdata: The private user data as set in Client() or userdata_set().
       :param msg: An instance of MQTTMessage, which contains the topic and payload.
       """

        from storage_heater.serializers import StorageHeaterSerializer

        payload = json.loads(msg.payload.decode('utf-8'))
        if payload['status']:
            try:
                serializer = StorageHeaterSerializer(data=payload)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    logger.info(f"{msg.topic} {msg.payload} has been saved to database")
            except ValidationError as error:
                logger.error(f'Failed validating data, with error message: {error},')
            except AssertionError as error:
                logger.error(f'Failed saving to db, with error message: {error},')
