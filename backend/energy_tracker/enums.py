from enum import Enum
from typing import TypeVar, Type

T = TypeVar('T', bound='BaseEnum')


class BaseEnum(Enum):
    @classmethod
    def from_string(cls: Type[T], name: str) -> int:
        """
        Convert string representation to enum value.

        Args:
            name: String identifier to convert

        Returns:
            int: The numeric value associated with the enum

        Raises:
            ValueError: If the identifier is invalid or not found
        """
        try:
            enum_name = name.upper()
            return cls[enum_name].value
        except KeyError:
            enum_type = cls.__name__
            raise ValueError(f"Invalid {enum_type} identifier: '{name}'. "
                             f"Valid values are: {[e.name.lower() for e in cls]}")


class RelayNumberMap(BaseEnum):
    RELAY_ONE = 1
    RELAY_TWO = 2
    RELAY_THREE = 3
    RELAY_FOUR = 4
    RELAY_FIVE = 5
    RELAY_SIX = 6

    @classmethod
    def name_to_number(cls, relay_name: str) -> int:
        """Convert relay name to its corresponding position number."""
        return cls.from_string(relay_name)


class PhaseRelayMap(BaseEnum):
    A = 2  # Phase A maps to relay 2
    B = 1  # Phase B maps to relay 1
    C = 3  # Phase C maps to relay 3

    @classmethod
    def name_to_number(cls, phase_name: str) -> int:
        """Maps a phase identifier to its corresponding relay number."""
        return cls.from_string(phase_name[-1])


class RelayAction(Enum):
    ON = "on"
    OFF = "off"

    def __str__(self) -> str:
        return self.value
