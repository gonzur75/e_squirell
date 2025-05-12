import json
import logging


from config import settings
import paho.mqtt.client as mqtt


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
        """ Connect to the MQTT broker using the provided client credentials and settings.
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
        from storage_heater.tasks import process_mqtt_payload
        try:
            if msg.payload:
                payload = json.loads(msg.payload)
                if payload and payload.get('status'):
                    process_mqtt_payload.delay(payload)

        except (AttributeError, json.JSONDecodeError) as e:
            logger.error(f'Failed decoding message payload: {e}')

    def start(self):
        self.connect()
        self.client.loop_start()


mqtt_client = mqtt.Client()
mqtt_service = MqttService(client=mqtt_client)
