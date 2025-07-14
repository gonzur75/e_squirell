import time

import machine

from config import RELAYS_PIN, RELAYS, SENSORS, TEMP_SENSOR
from helpers import log_and_restart


def get_status():
    """Get current system status including temperatures and relay states.

    Returns:
        dict: Combined dictionary containing system status, timestamp, temperatures and relay states
    """
    temps = read_temperature()
    relays = get_relays_status()
    return {'status': True,
            'time_stamp': time.time(),
            } | temps | relays


def read_temperature():
    """Read temperatures from all configured sensors.

    Converts and reads temperature values from each sensor with delay between readings.
    Handles potential errors by logging and restarting.

    Returns:
        dict: Dictionary with sensor names as keys and temperature values as values
    """
    TEMP_SENSOR.convert_temp()
    time.sleep_ms(750)  # time to allow for temp conversion
    temps = {}
    for name, address in SENSORS.items():
        try:
            temps[name] = TEMP_SENSOR.read_temp(address)
            time.sleep_ms(750)
        except Exception as e:
            log_and_restart(e)

    return temps


def handle_heating(relay_action, relay_number):
    """Control relay state for heating system.

    Args:
        relay_action (str): Action to perform on relay ('on' or 'off')
        relay_number (int): Number of the relay to control

    Returns:
        dict or str: Action status or error message if relay number is invalid
    """
    max_relays = len(RELAYS_PIN)
    if relay_number > max_relays:
        return f'We only have: {max_relays} relays. Please try again!'
    relay_key = RELAYS[relay_number -1]
    try:
        relay = machine.Pin(RELAYS_PIN[relay_key], machine.Pin.OUT)
        preform_action = getattr(relay, relay_action)
        preform_action()

    except Exception as e:
        log_and_restart(e)
    return {relay_number: relay_action}


def relay_state(pin):
    """Get current state of a relay pin.

    Args:
        pin (int): Pin number of the relay

    Returns:
        int: Current value of the relay pin (0 or 1)
    """
    relay = machine.Pin(pin, machine.Pin.OUT)
    return relay.value()


def get_relays_status():
    """Get status of all configured relays.

    Returns:
        dict: Dictionary with relay names as keys and their current states as values
    """
    return {name: relay_state(pin) for (name, pin) in RELAYS_PIN.items()}
