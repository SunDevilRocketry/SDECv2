# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass
from typing import Dict, Optional

from SDECv2.SerialController import SerialObj
from SDECv2.Sensor import create_sensors
from SDECv2.Sensor.util import process_data_bytes
from .engine_state import EngineState, parse_valve_byte

CONTROLLER_ID   = b"\x08"
CONTROLLER_NAME = "Liquid Engine Controller (L0002 Rev 5.0)"

_ACK    = b"\x95"
_NO_ACK = b"\x98"

_OPCODE_ABORT           = b"\x90"
_OPCODE_PREFLIGHT_PURGE = b"\x91"
_OPCODE_FILL_CHILL      = b"\x92"
_OPCODE_STANDBY         = b"\x93"
_OPCODE_HOTFIRE         = b"\x94"
_OPCODE_TELREQ          = b"\x96"
_OPCODE_STOP_PURGE      = b"\x97"
_OPCODE_GET_STATE       = b"\x99"
_OPCODE_STOP_HOTFIRE    = b"\x9A"
_OPCODE_LOX_PURGE       = b"\x9B"
_OPCODE_MANUAL          = b"\x9E"

_SENSOR_DUMP_SIZE = 40  # 10 sensors × 4 bytes each


@dataclass
class TelemetryData:
    """Snapshot of engine controller telemetry.

    :param sensor_readings: Mapping of sensor short-name to converted
        value in physical units (psi / lb / °C).
    :type sensor_readings: Dict[str, float]
    :param valve_states: Mapping of valve name to its current physical
        state string (``"OPEN"`` or ``"CLOSED"``).
    :type valve_states: Dict[str, str]
    """
    sensor_readings: Dict[str, float]
    valve_states: Dict[str, str]


def _send_state_command(serial: SerialObj, opcode: bytes) -> bool:
    """Send a single-byte opcode and return whether the controller acknowledged.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :param opcode: 1-byte command opcode.
    :type opcode: bytes
    :returns: ``True`` if the controller replied with ``ACK`` (``0x95``).
    :rtype: bool
    """
    serial.send(opcode)
    return serial.read() == _ACK


def hotfire_abort(serial: SerialObj) -> bool:
    """Send the abort command, transitioning the engine to ``ABORT`` state.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_ABORT)

def preflight_purge(serial: SerialObj) -> bool:
    """Initiate the pre-fire purge sequence (``PRE_FIRE_PURGE`` state).

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_PREFLIGHT_PURGE)

def fill_chill(serial: SerialObj) -> bool:
    """Initiate the fill-and-chill sequence (``FILL_AND_CHILL`` state).

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_FILL_CHILL)

def standby(serial: SerialObj) -> bool:
    """Transition the engine to ``STANDBY`` state.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_STANDBY)

def hotfire(serial: SerialObj) -> bool:
    """Initiate ignition, transitioning the engine to ``FIRE`` state.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_HOTFIRE)

def stop_hotfire(serial: SerialObj) -> bool:
    """Terminate the engine burn.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_STOP_HOTFIRE)

def stop_purge(serial: SerialObj) -> bool:
    """Stop the post-fire purge, transitioning the engine to ``DISARM`` state.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_STOP_PURGE)

def lox_purge(serial: SerialObj) -> bool:
    """Initiate the LOX tank purge sequence.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_LOX_PURGE)

def manual_mode(serial: SerialObj) -> bool:
    """Enter manual valve control mode (``MANUAL`` state).

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: ``True`` on acknowledgement.
    :rtype: bool
    """
    return _send_state_command(serial, _OPCODE_MANUAL)


def get_state(serial: SerialObj) -> Optional[EngineState]:
    """Query the current engine state from the controller.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: The current :class:`~SDECv2.EngineController.engine_state.EngineState`,
        or ``None`` on timeout, ``NACK``, or an unrecognized state byte.
    :rtype: Optional[EngineState]
    """
    serial.send(_OPCODE_GET_STATE)
    response = serial.read()
    if not response or response == _NO_ACK:
        return None
    try:
        return EngineState(response[0])
    except ValueError:
        return None


def telemetry_request(serial: SerialObj) -> Optional[TelemetryData]:
    """Request a snapshot of all sensor readings and valve states.

    Sends opcode ``0x96``, waits for ``ACK`` (``0x95``), then reads
    40 bytes of sensor data followed by 1 byte of valve state.
    Conversion functions are applied, so all sensor values are in
    physical units (psi / lb / °C).

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :returns: :class:`TelemetryData` containing converted sensor readings
        and decoded valve states, or ``None`` if the controller did not
        acknowledge.
    :rtype: Optional[TelemetryData]
    """
    serial.send(_OPCODE_TELREQ)
    if serial.read() != _ACK:
        return None

    sensor_data_bytes = serial.read(_SENSOR_DUMP_SIZE)
    valve_byte = serial.read()

    sensors = create_sensors.engine_controller_rev5_sensors()
    sensor_readings: Dict[str, float] = {}
    for sensor in sensors:
        raw = sensor_data_bytes[sensor.offset: sensor.offset + sensor.size]
        value = process_data_bytes(raw, sensor.data_type, sensor.convert_data)
        sensor_readings[sensor.short_name] = value

    valve_states = parse_valve_byte(valve_byte)
    return TelemetryData(sensor_readings=sensor_readings, valve_states=valve_states)
