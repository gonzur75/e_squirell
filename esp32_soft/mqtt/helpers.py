import machine
import time
import ubinascii
from umqtt.simple import MQTTClient

from heating import read_temperature, handle_heating


def connect_and_subscribe(topic_sub, mqtt_server, callback, client_id=None, keepalive=250):
    client_id = client_id if client_id is not None else ubinascii.hexlify(machine.unique_id())

    _client = MQTTClient(client_id, mqtt_server, keepalive)
    _client.set_callback(callback)
    _client.connect()
    _client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return _client


def restart_and_reconnect(e):
    print(f'Error {e}')
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def subscribe_callback(topic, msg):
    if msg == b'get_temps':
        temps = read_temperature(TEMP_SENSOR)
        CLIENT.publish(topic, temps)
    if msg.startswith('relay'):
        decoded_message = msg.decode('ascii')
        handle_heating(decoded_message[8:], int(decoded_message[6]))
        print(msg)
