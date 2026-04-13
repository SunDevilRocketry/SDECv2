# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import enum
import struct

from dataclasses import dataclass

from SDECv2.Sensor.create_sensors import rev2_dashboard_dump_sensors
from SDECv2.Sensor.sensor import Sensor
from SDECv2.Sensor.util import process_data_bytes
from typing import Dict

UID_SIZE = 12
LORA_INTERNAL_HEADER_SIZE = 20
LORA_PAYLOAD_SIZE = 76
LORA_MESSAGE_SIZE = LORA_INTERNAL_HEADER_SIZE + LORA_PAYLOAD_SIZE
FLIGHT_ID_SIZE = 16
VEHICLE_PADDING_SIZE = 54
DASHBOARD_PADDING_SIZE = 3


class LoRaMessageType(enum.IntEnum):
    """
    Message type IDs from the LoRa telemetry protocol.
    """

    VEHICLE_ID = 0x00000001
    DASHBOARD_DATA = 0x00000002
    WARNING_MESSAGE = 0x00000003
    INFO_MESSAGE = 0x00000004


@dataclass(frozen=True)
class LoRaInternalHeader:
    """
    Parsed LoRa message header.
    """

    uid: bytes
    mid: LoRaMessageType
    timestamp: int

    @classmethod
    def from_bytes(cls, data: bytes) -> "LoRaInternalHeader":
        """
        Parse a packed LoRa header from bytes.

        Args:
            data (bytes): Raw bytes containing exactly one header.

        Returns:
            LoRaInternalHeader: Parsed header values.
        """
        if len(data) != LORA_INTERNAL_HEADER_SIZE:
            raise ValueError("Error: Invalid LoRa header size")

        uid = data[:UID_SIZE]
        mid_raw = int.from_bytes(data[UID_SIZE : UID_SIZE + 4], "little")
        timestamp = int.from_bytes(data[UID_SIZE + 4 : UID_SIZE + 8], "little")

        try:
            mid = LoRaMessageType(mid_raw)
        except ValueError as exc:
            raise ValueError(f"Error: Unknown LoRa message type {mid_raw:#010x}") from exc

        return cls(uid=uid, mid=mid, timestamp=timestamp)


@dataclass(frozen=True)
class LoRaVehicleIdPayload:
    """
    Parsed vehicle ID payload.
    """

    hw_opcode: int
    fw_opcode: int
    version: int
    flight_id: str
    explicit_padding: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> "LoRaVehicleIdPayload":
        """
        Parse the vehicle ID payload.

        Args:
            data (bytes): Raw payload bytes.

        Returns:
            LoRaVehicleIdPayload: Parsed vehicle ID payload.
        """
        if len(data) != LORA_PAYLOAD_SIZE:
            raise ValueError("Error: Invalid vehicle ID payload size")

        hw_opcode, fw_opcode, version = struct.unpack("<BBI", data[:6])
        flight_id_bytes = data[6 : 6 + FLIGHT_ID_SIZE]
        flight_id = flight_id_bytes.split(b"\x00", 1)[0].decode("ascii", errors="ignore")
        explicit_padding = data[6 + FLIGHT_ID_SIZE : 6 + FLIGHT_ID_SIZE + VEHICLE_PADDING_SIZE]

        return cls(
            hw_opcode=hw_opcode,
            fw_opcode=fw_opcode,
            version=version,
            flight_id=flight_id,
            explicit_padding=explicit_padding,
        )


@dataclass(frozen=True)
class LoRaTextMessagePayload:
    """
    Parsed text payload used for warning and info messages.
    """

    msg: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> "LoRaTextMessagePayload":
        """
        Parse the text payload bytes.

        Args:
            data (bytes): Raw payload bytes.

        Returns:
            LoRaTextMessagePayload: Parsed text message payload.
        """
        if len(data) != LORA_PAYLOAD_SIZE:
            raise ValueError("Error: Invalid text message payload size")

        return cls(msg=data)


@dataclass(frozen=True)
class LoRaDashboardDumpPayload:
    """
    Parsed dashboard dump payload.
    """

    fsm_state: int
    data: Dict[Sensor, float | int | None]
    explicit_padding: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> "LoRaDashboardDumpPayload":
        """
        Parse the dashboard dump payload from bytes.

        Args:
            data (bytes): Raw payload bytes.

        Returns:
            LoRaDashboardDumpPayload: Parsed dashboard dump payload.
        """
        if len(data) != LORA_PAYLOAD_SIZE:
            raise ValueError("Error: Invalid dashboard dump payload size")

        fsm_state = data[0]
        dashboard_bytes = data[1 : 1 + (LORA_PAYLOAD_SIZE - 1 - DASHBOARD_PADDING_SIZE)]
        explicit_padding = data[-DASHBOARD_PADDING_SIZE:]

        sensors = rev2_dashboard_dump_sensors()
        parsed_data: Dict[Sensor, float | int | None] = {}
        for sensor in sensors:
            sensor_data_bytes = dashboard_bytes[sensor.offset : sensor.offset + sensor.size]
            parsed_data[sensor] = process_data_bytes(
                sensor_data_bytes, sensor.data_type, sensor.convert_data
            )

        return cls(fsm_state=fsm_state, data=parsed_data, explicit_padding=explicit_padding)


@dataclass(frozen=True)
class LoRaMessage:
    """
    Parsed packed LoRa message with header and union payload.
    """

    header: LoRaInternalHeader
    payload: LoRaVehicleIdPayload | LoRaDashboardDumpPayload | LoRaTextMessagePayload

    @classmethod
    def from_bytes(cls, data: bytes) -> "LoRaMessage":
        """
        Parse a full packed LoRa message.

        Args:
            data (bytes): Raw bytes containing exactly one message.

        Returns:
            LoRaMessage: Parsed LoRa message.
        """
        if len(data) != LORA_MESSAGE_SIZE:
            raise ValueError("Error: Invalid LoRa message size")

        header_bytes = data[:LORA_INTERNAL_HEADER_SIZE]
        payload_bytes = data[LORA_INTERNAL_HEADER_SIZE:]

        header = LoRaInternalHeader.from_bytes(header_bytes)
        if header.mid == LoRaMessageType.VEHICLE_ID:
            payload = LoRaVehicleIdPayload.from_bytes(payload_bytes)
        elif header.mid == LoRaMessageType.DASHBOARD_DATA:
            payload = LoRaDashboardDumpPayload.from_bytes(payload_bytes)
        else:
            payload = LoRaTextMessagePayload.from_bytes(payload_bytes)

        return cls(header=header, payload=payload)
