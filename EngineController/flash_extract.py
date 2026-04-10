# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import struct
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List

from SDECv2.SerialController import SerialObj
from SDECv2.Sensor import create_sensors
from SDECv2.Sensor.util import process_data_bytes

FLASH_SIZE = 524288  # 512 KB

# Frame layout: 4-byte uint32 timestamp + 10 × int32 sensor values = 44 bytes
_FRAME_FORMAT  = "<I10i"
_FRAME_SIZE    = struct.calcsize(_FRAME_FORMAT)  # 44 bytes

_SENSOR_NAMES = [s.short_name for s in create_sensors.engine_controller_rev5_sensors()]

_OPCODE_FLASH   = b"\x22"
_SUBCODE_EXTRACT = b"\xC0"

# An erased flash cell reads as 0xFF; a timestamp of all 0xFF means empty
_EMPTY_TIMESTAMP = 0xFFFFFFFF


@dataclass
class EngineControllerFlashFrame:
    """A single parsed telemetry frame from engine controller flash memory.

    :param timestamp_ms: Time since launch in milliseconds, as recorded
        by the engine controller.
    :type timestamp_ms: int
    :param sensor_readings: Mapping of sensor short-name to converted
        value in physical units (psi / lb / °C).
    :type sensor_readings: Dict[str, float]
    """
    timestamp_ms: int
    sensor_readings: Dict[str, float]


def flash_extract(serial: SerialObj, store_data: bool = False,
                  output_path: str = "a_output/engine_ctrl_rev5_flash_data.csv"
                  ) -> List[EngineControllerFlashFrame]:
    """Download and parse the full flash contents of the engine controller.

    Sends opcode ``0x22`` with sub-command ``0xC0``, then reads 512 KB of
    flash in 512-byte chunks. Each 44-byte frame is structured as::

        uint32  timestamp_ms   (4 bytes)
        int32   pt0 … lc       (10 × 4 bytes)

    Conversion functions are applied so all returned sensor values are in
    physical units (psi / lb / °C). Frames whose timestamp equals
    ``0xFFFFFFFF`` (erased flash) are discarded.

    :param serial: Open serial connection to the engine controller.
    :type serial: SerialObj
    :param store_data: When ``True``, write the parsed frames to *output_path*
        as a CSV file.
    :type store_data: bool
    :param output_path: Destination path for the CSV output.
    :type output_path: str
    :returns: List of parsed :class:`EngineControllerFlashFrame` objects in
        chronological order.
    :rtype: List[EngineControllerFlashFrame]
    """
    serial.send(_OPCODE_FLASH)
    serial.send(_SUBCODE_EXTRACT)

    num_chunks = FLASH_SIZE // 512
    flash_bytes = bytearray()
    for i in range(num_chunks):
        if i % 128 == 0:
            print(f"Reading block {i} ...")
        chunk = serial.read(num_bytes=512)
        num_received = len(chunk)
        if num_received == 0:
            print(f"[{i + 1}/{num_chunks}] Timeout: flash appears empty")
        elif num_received != 512:
            print(f"[{i + 1}/{num_chunks}] Partial read ({num_received} bytes)")
        flash_bytes.extend(chunk)

    print(f"{len(flash_bytes)} bytes received from flash")

    # Consume the trailing status byte
    serial.read()

    sensors = create_sensors.engine_controller_rev5_sensors()
    frames: List[EngineControllerFlashFrame] = []
    frame_dicts = []

    offset = 0
    while offset + _FRAME_SIZE <= len(flash_bytes):
        raw = struct.unpack(_FRAME_FORMAT, flash_bytes[offset: offset + _FRAME_SIZE])
        offset += _FRAME_SIZE

        timestamp_ms = raw[0]
        if timestamp_ms == _EMPTY_TIMESTAMP:
            continue

        raw_sensor_values = raw[1:]
        sensor_readings: Dict[str, float] = {}
        for sensor, raw_val in zip(sensors, raw_sensor_values):
            value = process_data_bytes(
                raw_val.to_bytes(sensor.size, byteorder="little", signed=True),
                sensor.data_type,
                sensor.convert_data,
            )
            sensor_readings[sensor.short_name] = value

        frames.append(EngineControllerFlashFrame(timestamp_ms, sensor_readings))
        if store_data:
            frame_dicts.append({"timestamp_ms": timestamp_ms, **sensor_readings})

    if store_data and frame_dicts:
        pd.DataFrame(frame_dicts).to_csv(output_path, index=False)
        print(f"Flash data saved to {output_path}")

    print(f"{len(frames)} valid frames parsed")
    return frames
