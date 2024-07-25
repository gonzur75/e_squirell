# Complete project details at https://RandomNerdTutorials.com
import time
import micropython
import ubinascii

import machine
import onewire
import ds18x20
from umqttsimple import MQTTClient

MQTT_SERVER = "192.168.8.2"  # 'YOUR_MQTT_BROKER_IP'
TOPIC = b'heat_storage'
cllient_id = ubinascii.hexlify(machine.unique_id())

def sub_cb(topic, msg):
    print((topic, msg))
    if msg == b'get_temps':
        print('Sending temps received hello message')


def connect_and_subscribe(topic_sub, mqtt_server, client_id=None):
    client_id = client_id if client_id is not None else ubinascii.hexlify(machine.unique_id())

    _client = MQTTClient(client_id, mqtt_server)

    _client.set_callback(sub_cb)
    _client.connect()
    _client.subscribe(b'heat_storage_services')
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return _client


def restart_and_reconnect(e):
    print(f'Error {e}')
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def read_temperature():
    thermometer = onewire.OneWire(machine.Pin(14))
    ds = ds18x20.DS18X20(thermometer)
    readings = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)


try:
    client = connect_and_subscribe(TOPIC, MQTT_SERVER, cllient_id)
except OSError as e:
    restart_and_reconnect(e)


def run(message_interval=5):
    last_message = 0
    counter = 0

    def run_instance_():
        nonlocal last_message

        try:
            client.check_msg()

            if (time.time() - last_message) > message_interval:
                msg = b'Hello'
                print(f'sending messsage')
                client.publish(TOPIC, msg)
                last_message = time.time()

        except OSError as e:
            restart_and_reconnect(e)

        return

    return run_instance_


run_instance = run()

while True:
    run_instance()
