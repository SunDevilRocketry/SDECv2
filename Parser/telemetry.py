# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

"""
Packed LoRa wire layout (little-endian floats and integers), mirroring flight-computer C structs.
ST_UID_TYPE is modeled as 12 opaque bytes (sizeof header is 20 == 12 + 4 + 4).
Struct padding bytes on the wire are not retained on parsed payloads.
"""

from __future__ import annotations

import enum
import struct
from dataclasses import dataclass, asdict
from typing import ClassVar
from SDECv2.SerialController import SerialObj
from SDECv2.BaseController import create_controllers, create_firmwares
from threading import Lock
from typing import Any

UID_SIZE = 12
LORA_INTERNAL_HEADER_SIZE = 20
LORA_PAYLOAD_SIZE = 76
LORA_MESSAGE_SIZE = LORA_INTERNAL_HEADER_SIZE + LORA_PAYLOAD_SIZE
FLIGHT_ID_SIZE = 16
DASHBOARD_DUMP_TYPE_SIZE = 72

class LoRaMessageTypes(enum.IntEnum):
    """LORA_MESSAGE_TYPES (uint32 on wire)."""
    NULL_MSG = 0x00000000
    VEHICLE_ID = 0x00000001
    DASHBOARD_DATA = 0x00000002
    WARNING_MESSAGE = 0x00000003
    INFO_MESSAGE = 0x00000004


@dataclass(frozen=True)
class LoRaInternalHeaderType:
    """LORA_INTERNAL_HEADER_TYPE — uid, mid, timestamp (packed, 20 bytes)."""

    STRUCT: ClassVar[str] = f"<{UID_SIZE}sII"

    uid: bytes
    mid: int
    timestamp: int

    @property
    def mid_enum(self) -> LoRaMessageTypes | None:
        try:
            return LoRaMessageTypes(self.mid)
        except ValueError:
            return None

    @classmethod
    def parse(cls, data: bytes) -> LoRaInternalHeaderType:
        if len(data) < LORA_INTERNAL_HEADER_SIZE:
            raise ValueError(
                f"LoRaInternalHeaderType.parse expects {LORA_INTERNAL_HEADER_SIZE} bytes, "
                f"got {len(data)}"
            )
        uid, mid_u32, ts = struct.unpack(cls.STRUCT, data[:LORA_INTERNAL_HEADER_SIZE])
        return cls(bytes(uid), mid_u32, ts)


@dataclass(frozen=True)
class DashboardDumpType:
    """DASHBOARD_DUMP_TYPE — 18 × float32, 72 bytes."""

    STRUCT: ClassVar[str] = "<18f"

    accXconv: float
    accYconv: float
    accZconv: float
    gyroXconv: float
    gyroYconv: float
    gyroZconv: float
    rollDeg: float
    pitchDeg: float
    yawDeg: float
    rollRate: float
    pitchRate: float
    yawRate: float
    pres: float
    temp: float
    alt: float
    bvelo: float
    longitude: float
    latitude: float

    @classmethod
    def parse(cls, data: bytes) -> DashboardDumpType:
        if len(data) < DASHBOARD_DUMP_TYPE_SIZE:
            raise ValueError(
                f"DashboardDumpType.parse expects {DASHBOARD_DUMP_TYPE_SIZE} bytes, got {len(data)}"
            )
        unpacked = struct.unpack(cls.STRUCT, data[:DASHBOARD_DUMP_TYPE_SIZE])
        return cls(*unpacked)
    
    def to_json(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class LoRaMsgVehicleIdType:
    """LORA_MSG_VEHICLE_ID_TYPE — trailing explicit padding on the wire is discarded."""

    STRUCT: ClassVar[str] = "<BBI16s"

    hw_opcode: int
    fw_opcode: int
    version: int
    flight_id: str

    @classmethod
    def parse(cls, data: bytes) -> LoRaMsgVehicleIdType:
        if len(data) < LORA_PAYLOAD_SIZE:
            raise ValueError(
                f"LoRaMsgVehicleIdType.parse expects {LORA_PAYLOAD_SIZE} bytes, got {len(data)}"
            )
        hw, fw, ver, fid = struct.unpack(cls.STRUCT, data[: 6 + FLIGHT_ID_SIZE])
        flight_id = fid.split(b"\x00", 1)[0].decode("utf-8", errors="replace")
        return cls(hw, fw, ver, flight_id)


@dataclass(frozen=True)
class LoRaMsgDashboardDumpType:
    """LORA_MSG_DASHBOARD_DUMP_TYPE — trailing explicit padding on the wire is discarded."""

    fsm_state: int
    data: DashboardDumpType

    @classmethod
    def parse(cls, data: bytes) -> LoRaMsgDashboardDumpType:
        if len(data) < LORA_PAYLOAD_SIZE:
            raise ValueError(
                f"LoRaMsgDashboardDumpType.parse expects {LORA_PAYLOAD_SIZE} bytes, got {len(data)}"
            )
        fsm_state = data[0]
        dash = DashboardDumpType.parse(data[1 : 1 + DASHBOARD_DUMP_TYPE_SIZE])
        return cls(fsm_state, dash)


@dataclass(frozen=True)
class LoRaMsgTextMessageType:
    """LORA_MSG_TEXT_MESSAGE_TYPE — TEXT_MESSAGE occupies the full 76-byte slot."""

    msg: str

    @classmethod
    def parse(cls, data: bytes) -> LoRaMsgTextMessageType:
        if len(data) < LORA_PAYLOAD_SIZE:
            raise ValueError(
                f"LoRaMsgTextMessageType.parse expects {LORA_PAYLOAD_SIZE} bytes, got {len(data)}"
            )
        raw = data[:LORA_PAYLOAD_SIZE]
        msg = raw.decode("utf-8", errors="replace").rstrip("\x00")
        return cls(msg)


@dataclass(frozen=True)
class LoRaMessage:
    """LORA_MESSAGE — header plus one branch of the payload union."""

    header: LoRaInternalHeaderType
    vehicle_id: LoRaMsgVehicleIdType | None = None
    dashboard_dump: LoRaMsgDashboardDumpType | None = None
    text_message: LoRaMsgTextMessageType | None = None
    raw_payload: bytes | None = None

    @classmethod
    def parse(cls, data: bytes) -> LoRaMessage:
        if len(data) < LORA_MESSAGE_SIZE:
            raise ValueError(
                f"LoRaMessage.parse expects at least {LORA_MESSAGE_SIZE} bytes, got {len(data)}"
            )
        chunk = data[:LORA_MESSAGE_SIZE]
        header = LoRaInternalHeaderType.parse(chunk[:LORA_INTERNAL_HEADER_SIZE])
        payload = chunk[LORA_INTERNAL_HEADER_SIZE:LORA_MESSAGE_SIZE]

        vehicle_id = None
        dashboard_dump = None
        text_message = None
        raw_payload: bytes | None = None

        match header.mid_enum:
            case LoRaMessageTypes.VEHICLE_ID:
                vehicle_id = LoRaMsgVehicleIdType.parse(payload)
            case LoRaMessageTypes.DASHBOARD_DATA:
                dashboard_dump = LoRaMsgDashboardDumpType.parse(payload)
            case LoRaMessageTypes.WARNING_MESSAGE | LoRaMessageTypes.INFO_MESSAGE:
                text_message = LoRaMsgTextMessageType.parse(payload)
            case _:
                raw_payload = bytes(payload)

        return cls(
            header,
            vehicle_id=vehicle_id,
            dashboard_dump=dashboard_dump,
            text_message=text_message,
            raw_payload=raw_payload,
        )

class Telemetry:
    """
    Class to manage dashboard commands (SDECv2 -> USB -> Flight Computer) 
                                    || (SDECv2 -> USB -> Ground Station -> LoRa -> Flight Computer)
    
    Singleton. One global instance is available.
    """
    instance = None

    def __new__(cls):
        if( cls.instance is None ):
            cls.instance = super().__new__(cls)
            return cls.instance
        else:
            return cls.instance
        
    def __init__(self):
        if(hasattr(self, 'last_dashboard_dump')): # guard
            return
        self.telem_lock = Lock()
        self.last_dashboard_dump = None
        self.last_wireless_stats = {
                "target": "Connecting...",
                "firmware": "Connecting...",
                "latency": 0,
                "sig_strength": 0,
                "status": "Connecting..."
                }
        self.last_msg_time = None

    def dashboard_dump(self, serial_connection: SerialObj):
        """
        Perform the dashboard dump command on the connected target (FC or GS). Data populates to an instance variable for
        thread safety. Use dashboard_dump() and get_latest_dashboard_dump() in sequence to retrieve data.

        serial_connection: A SerialObj to communicate with the target on. Requires a completed connect() command.
        """
        serial_connection.send(b'\x30')
        if( serial_connection.target == None ):
            print("Warning: The serial connection does not have an associated hardware/firmware platform. Report this.")
        elif( serial_connection.target.controller.id == b'\x05'):
            # Flight Computer: Parse dashboard dump
            data = serial_connection.read(DASHBOARD_DUMP_TYPE_SIZE)
            parsed = DashboardDumpType.parse(data)
            with( self.telem_lock ):
                self.last_dashboard_dump = parsed
        elif( serial_connection.target.controller.id == b'\x10'):
            # Ground station: Interpret message & save
            data = serial_connection.read(LORA_MESSAGE_SIZE)
            parsed = LoRaMessage.parse(data)

            with( self.telem_lock ):

                # Update latency timer
                if( self.last_msg_time == None ):
                    self.last_msg_time = parsed.header.timestamp
                else:
                    self.last_wireless_stats.update({"latency": parsed.header.timestamp - self.last_msg_time})
                    self.last_msg_time = parsed.header.timestamp

                # Update message
                if( parsed.header.mid_enum == LoRaMessageTypes.DASHBOARD_DATA ):
                    self.last_dashboard_dump = parsed.dashboard_dump.data
                elif( parsed.header.mid_enum == LoRaMessageTypes.VEHICLE_ID ):
                    self.last_wireless_stats = {
                    "target": create_controllers.create_controller(parsed.vehicle_id.hw_opcode).name,
                    "firmware": create_firmwares.create_firmware(parsed.vehicle_id.fw_opcode).name,
                    "latency": self.last_wireless_stats["latency"],
                    "sig_strength": 0,
                    "status": "OK"
                    }
    
    def get_latest_dashboard_dump(self) -> dict[str, Any] | None:
        with( self.telem_lock ):
            to_return = self.last_dashboard_dump

        if( to_return != None ): # extra None guard since dashboard dump is a dataclass
            to_return = to_return.to_json()
        return to_return
    
    def get_latest_wireless_stats(self) -> dict[str, Any]:
        with( self.telem_lock ):
            to_return = self.last_wireless_stats

        return to_return
