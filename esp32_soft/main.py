# Complete project details at https://RandomNerdTutorials.com
import time
import micropython

import machine
import onewire
import ds18x20
from umqttsimple import MQTTClient


def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client


def restart_and_reconnect(e):
    print(f'Error {e}')
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


# try:
#   client = connect_and_subscribe()
# except OSError as e:
#   restart_and_reconnect(e)

while True:
    thermometer = onewire.OneWire(machine.Pin(14))
    ds = ds18x20.DS18X20(thermometer)
    readings = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    for read in readings:
        print(ds.read_temp(read))

    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect(e)
