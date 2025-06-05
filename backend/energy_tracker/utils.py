import json
from datetime import datetime
from typing import Collection, Sequence, Generator

from django.conf import settings
from paho.mqtt import publish as publish

from core.utils import get_project_settings
from energy_tracker.enums import RelayAction, PhaseRelayMap, RelayNumberMap
from storage_heater.models import StorageHeater

import pytz

project_settings = get_project_settings()

# Constants
VOLTAGE_CONTROL_HOURS_START = 8
VOLTAGE_CONTROL_HOURS_END = 18
TIMEZONE = 'Europe/Warsaw'


def get_phases_requiring_stabilization(voltage_per_phase: list[tuple[str, float]]) -> tuple[int, ...] | bool:
    """
    Check which phases require voltage stabilization during voltage control hours.
    
    Args:
        voltage_per_phase: List of tuples containing phase name and voltage value
        
    Returns:
        Tuple of phase names requiring stabilization during voltage control hours,
        or False if no stabilization is needed or outside control hours
    """
    voltage_threshold = project_settings.voltage_threshold
    current_hour = datetime.now(pytz.timezone(TIMEZONE)).hour

    phases_over_threshold = tuple(
        PhaseRelayMap.name_to_number(phase_name)
        for phase_name, voltage in voltage_per_phase
        if voltage > voltage_threshold
    )

    is_control_period = VOLTAGE_CONTROL_HOURS_START <= current_hour < VOLTAGE_CONTROL_HOURS_END

    if is_control_period and phases_over_threshold:
        return phases_over_threshold

    return False


def get_phases_below_safe_voltage(voltage_readings: Sequence[tuple[str, float]]) -> tuple[int, ...]:
    """
    Identifies power phases that are below the safe voltage threshold.
    
    Args:
        voltage_readings: Sequence of tuples containing (phase_name, voltage_value)
    
    Returns:
        Tuple of relay numbers corresponding to phases with voltage below safe threshold
    """
    safe_voltage_threshold = settings.safe_voltage_threshold

    unsafe_phases = tuple(
        PhaseRelayMap.name_to_number(phase_name)
        for phase_name, voltage in voltage_readings
        if voltage < safe_voltage_threshold
    )
    return unsafe_phases


def check_heating_state() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """
    Check the current state of storage heaters and return their relay numbers.
    
    Returns:
        Tuple containing two tuples:
        - First tuple: Active 1kW heater relay numbers
        - Second tuple: Active 2kW heater relay numbers
    """

    def get_active_relays(_relay_states: dict, start_idx: int, end_idx: int) -> tuple[int, ...]:
        """Helper function to get active relay numbers for a specific range."""
        return tuple(
            RelayNumberMap.name_to_number(relay_name)
            for relay_name, is_active in list(_relay_states.items())[start_idx:end_idx]
            if is_active
        )

    relay_fields: Generator[str] = (
        field.name for field in StorageHeater._meta.get_fields()
        if field.name.startswith('relay_')
    )

    relay_states = StorageHeater.objects.values(*relay_fields).first()

    # First 3 relays are 1kW heaters, last 3 are 2kW heaters
    one_kw_heaters = get_active_relays(relay_states, start_idx=0, end_idx=3)
    two_kw_heaters = get_active_relays(relay_states, start_idx=3, end_idx=6)

    return one_kw_heaters, two_kw_heaters


def process_smart_meter_data(data: dict):
    # negate value as smart_meter returns negative if production is more than consumption
    active_power = -data.get("total_active_power", 0)
    heating_required = project_settings.heating_required
    # [('voltage_a', 2134),  ...]

    voltage_per_phase: list[tuple[str, int]] = sorted(
        (x for x in data.items() if x[0] in ('voltage_a', 'voltage_b', 'voltage_c')),
        key=lambda x: x[1], reverse=True)

    relay_numbers_matched_to_phases = tuple(PhaseRelayMap.name_to_number(phase[0]) for phase in voltage_per_phase)

    if phases_to_stabilize := get_phases_requiring_stabilization(voltage_per_phase):
        one_kw_heaters_on, two_kw_heaters_on = check_heating_state()

        if one_kw_heaters_on and two_kw_heaters_on:
            turn_off_relays(one_kw_heaters_on + two_kw_heaters_on)

        elif one_kw_heaters_on and not two_kw_heaters_on:
            if (
                    len(one_kw_heaters_on) == 1
                    and len(phases_to_stabilize) == 1
                    and one_kw_heaters_on == two_kw_heaters_on
            ):
                send_relay_action(one_kw_heaters_on[0] + 3, RelayAction.ON)
                send_relay_action(one_kw_heaters_on[0], RelayAction.OFF)


            elif relays_on := set(phases_to_stabilize).difference(one_kw_heaters_on):
                turn_on_relays(relays_on)

        else:
            turn_on_relays(phases_to_stabilize)

    if not heating_required and (safe_range_phases := get_phases_below_safe_voltage(voltage_per_phase)):
        turn_off_relays(safe_range_phases)

    if heating_required:

        if active_power > 2400:
            update_relay_sequence(3, relay_numbers_matched_to_phases)

        elif active_power > 1600:
            update_relay_sequence(2, relay_numbers_matched_to_phases)

        elif active_power > 800:
            update_relay_sequence(1, relay_numbers_matched_to_phases)

    return True


def update_relay_sequence(relays_on: int, relay_list: tuple[int, ...]) -> bool:
    """
    Updates a sequence of relays by turning on the first N relays and turning off the rest.
    
    Args:
        relays_on: Number of relays to turn on (from the start of the sequence)
        relay_list: Tuple of relay numbers to control
        
    Returns:
        bool: True if relay states were updated successfully
        
    Raises:
        ValueError: If relays_on is negative or greater than the number of relays
    """
    if not 0 <= relays_on <= len(relay_list):
        raise ValueError(f"relays_on must be between 0 and {len(relay_list)}")

    def set_relay_range(relay_numbers: tuple[int, ...], action: RelayAction) -> None:
        for relay_number in relay_numbers:
            send_relay_action(relay_number, action)

    set_relay_range(relay_list[:relays_on], RelayAction.ON)

    set_relay_range(relay_list[relays_on:], RelayAction.OFF)

    return True


def send_relay_action(relay_number: int, relay_action: RelayAction = RelayAction.ON) -> None:
    """
       Publishes an MQTT message to control a specific heating relay.

       Args:
           relay_number (int): The identifier of the relay (e.g., 1, 2).
           relay_action (str, optional): The desired state of the relay ('on' or 'off').
                                       Defaults to 'on'.
   """

    payload = {"heating_action": f'relay_{relay_number}_{relay_action}'}
    publish.single(settings.MQTT_TOPIC, json.dumps(payload), hostname=settings.MQTT_SERVER)
    return None


def turn_off_relays(relays: Collection[int]) -> None:
    """
    Turn off multiple relays in sequence.

    Args:
        relays: An iterable of relay numbers to turn off

    Raises:
        ValueError: If relays iterable is empty
    """

    if not relays:
        raise ValueError("Relays iterable cannot be empty")

    for relay in relays:
        send_relay_action(relay, RelayAction.OFF)


def turn_on_relays(relays: Collection[int]) -> None:
    """
    Activate multiple relays by setting them to ON state.

    Args:
        relays: Collection of relay numbers to be turned on

    Example:
        turn_on_relays([1, 2, 3]) # Turns on relays 1, 2, and 3
    """
    if not relays:
        raise ValueError("Relays iterable cannot be empty")

    for relay in relays:
        send_relay_action(relay, RelayAction.ON)
