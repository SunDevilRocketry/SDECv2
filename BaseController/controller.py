# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .base_sensor import BaseSensor
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Controller:
    id: bytes
    name: str
    poll_codes: Dict[bytes, BaseSensor]
    sensor_frame_size: int
    sensor_data_file: str

    def __str__(self):
        return (
            "Controller:{" +
            f"\n ID: {self.id}" +
            f"\n Name: {self.name}" +
            f"\n Sensor Frame Size: {self.sensor_frame_size}" +
            f"\n Sensor Data File: {self.sensor_data_file}" +
            "\n}"
        )
    
    def raw_bytes_repr(self, byte: bytes) -> str:
        return "b'" + "".join(f"\\x{b:02x}" for b in byte) + "'"
        
    def get_formatted_poll_codes(self):
        to_return = []
        for byte, sensor in self.poll_codes.items():
            to_return.append(f"{self.raw_bytes_repr(byte)} : {sensor}")
        
        return "\n".join(to_return)