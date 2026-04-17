# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass
from enum import IntEnum
from typing import Dict


class EngineState(IntEnum):
    """Engine controller state machine states.

    States progress through the nominal hotfire sequence:
    ``INITIALIZATION`` → ``READY`` → ``PRE_FIRE_PURGE`` → ``FILL_AND_CHILL``
    → ``STANDBY`` → ``FIRE`` → ``DISARM`` → ``POST_FIRE``.

    ``MANUAL`` and ``ABORT`` are reachable from any state.
    """
    INITIALIZATION = 0x00
    READY          = 0x01
    PRE_FIRE_PURGE = 0x02
    FILL_AND_CHILL = 0x03
    STANDBY        = 0x04
    FIRE           = 0x05
    DISARM         = 0x06
    POST_FIRE      = 0x07
    MANUAL         = 0x08
    ABORT          = 0x09


#: Human-readable display names for each :class:`EngineState`.
ENGINE_STATE_NAMES: Dict[EngineState, str] = {
    EngineState.INITIALIZATION: "Initialization",
    EngineState.READY:          "Ready",
    EngineState.PRE_FIRE_PURGE: "Pre-Fire Purge",
    EngineState.FILL_AND_CHILL: "Fill and Chill",
    EngineState.STANDBY:        "Standby",
    EngineState.FIRE:           "Fire",
    EngineState.DISARM:         "Disarm",
    EngineState.POST_FIRE:      "Post-Fire",
    EngineState.MANUAL:         "Manual",
    EngineState.ABORT:          "Abort",
}


@dataclass(frozen=True)
class Valve:
    """Metadata for a single solenoid valve.

    :param name: Valve identifier string (e.g. ``"oxPress"``).
    :param on_state: Physical state when the valve bit is **set**
        (e.g. ``"OPEN"`` or ``"CLOSED"``).
    :param off_state: Physical state when the valve bit is **clear**.
    """
    name: str
    on_state: str
    off_state: str


#: All eight valves keyed by 1-indexed bit position in the telemetry valve byte.
#: Bit *n* maps to ``(1 << (n - 1))`` in the byte returned by
#: :func:`~SDECv2.EngineController.engine_controller.telemetry_request`.
VALVES: Dict[int, Valve] = {
    1: Valve("oxPress",   "OPEN",   "CLOSED"),
    2: Valve("fuelPress", "OPEN",   "CLOSED"),
    3: Valve("oxVent",    "CLOSED", "OPEN"),
    4: Valve("fuelVent",  "CLOSED", "OPEN"),
    5: Valve("oxPurge",   "CLOSED", "OPEN"),
    6: Valve("fuelPurge", "CLOSED", "OPEN"),
    7: Valve("oxMain",    "OPEN",   "CLOSED"),
    8: Valve("fuelMain",  "OPEN",   "CLOSED"),
}


def parse_valve_byte(valve_byte: bytes) -> Dict[str, str]:
    """Decode the 1-byte valve bitmask from telemetry into a valve name → state mapping.

    :param valve_byte: Single byte received from the engine controller where
        each bit represents one valve's state (bit 0 = valve 1, etc.).
    :type valve_byte: bytes
    :returns: Mapping of valve name to its physical state string
        (``"OPEN"`` or ``"CLOSED"``).
    :rtype: Dict[str, str]
    """
    valve_int = valve_byte[0]
    states: Dict[str, str] = {}
    for bit_pos, valve in VALVES.items():
        if valve_int & (1 << (bit_pos - 1)):
            states[valve.name] = valve.on_state
        else:
            states[valve.name] = valve.off_state
    return states
