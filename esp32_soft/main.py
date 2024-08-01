# Complete project details at https://RandomNerdTutorials.com
import time
import ubinascii
import machine
from umqttsimple import MQTTClient

MQTT_SERVER = SECRETS['mqtt']['server']
TOPIC = b'heat_storage'


def connect_and_subscribe(topic_sub, mqtt_server, client_id=None):
    client_id = client_id if client_id is not None else ubinascii.hexlify(machine.unique_id())

    _client = MQTTClient(client_id, mqtt_server)
    _client.set_callback(sub_cb)
    _client.connect()
    _client.subscribe(TOPIC)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return _client


def restart_and_reconnect(e):
    print(f'Error {e}')
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def read_temperature(temp_sensor):
    readings = temp_sensor.scan()
    temp_sensor.convert_temp()
    time.sleep_ms(750)  # time to allow for temp conversion
    temperatures = map(lambda reading: str(temp_sensor.read_temp(reading)), readings)
    return ' '.join(temperatures)


def handle_heating(relay_action, relay_number):
    print(relay_number)
    max_relays = len(RELAYS_PIN)
    if relay_number > max_relays:
        msg = f'We only have: {max_relays} relays. Please try again!'
        client.publish(TOPIC, msg)
        return
    relay = machine.Pin(RELAYS_PIN[relay_number - 1], machine.Pin.OUT)
    preform_action = getattr(relay, relay_action)
    preform_action()



def sub_cb(topic, msg):
    if msg == b'get_temps':
        temps = read_temperature(TEMP_SENSOR)
        client.publish(TOPIC, temps)
    if msg.startswith('relay'):
        decoded_message = msg.decode('ascii')
        handle_heating(decoded_message[8:], int(decoded_message[6]))
        print(msg)


try:
    print('Setting up mqtt connection')
    client = connect_and_subscribe(TOPIC, MQTT_SERVER)
except OSError as e:
    restart_and_reconnect(e)


def run(message_interval=5):
    last_message = 0

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
