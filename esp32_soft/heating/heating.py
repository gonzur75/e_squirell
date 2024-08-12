import time

import machine

from config import RELAYS_PIN, SENSORS, TEMP_SENSOR


def get_status():
    temps = read_temperature()
    relays = get_relays_status()
    return {'status': True,
            'time_stamp': time.time(),
            } | temps | relays


def read_temperature():
    TEMP_SENSOR.convert_temp()
    time.sleep_ms(750)  # time to allow for temp conversion

    return {name: TEMP_SENSOR.read_temp(address) for (name, address) in SENSORS.items()}


def handle_heating(relay_action, relay_number):
    print(relay_number)
    max_relays = len(RELAYS_PIN)
    if relay_number > max_relays:
        return f'We only have: {max_relays} relays. Please try again!'

    relay = machine.Pin(RELAYS_PIN[relay_number - 1], machine.Pin.OUT)
    preform_action = getattr(relay, relay_action)
    preform_action()
    return {relay_number: relay_action}


def relay_state(pin):
    relay = machine.Pin(pin, machine.Pin.OUT)
    return relay.value()


def get_relays_status():
    return {name: relay_state(pin) for (name, pin) in RELAYS_PIN.items()}
