import time

import machine

from config import RELAYS_PIN, TOPIC


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
        return f'We only have: {max_relays} relays. Please try again!'

    relay = machine.Pin(RELAYS_PIN[relay_number - 1], machine.Pin.OUT)
    preform_action = getattr(relay, relay_action)
    preform_action()
    return f'Relay {relay_number}: {relay_action}'
