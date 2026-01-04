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
            "\n ID: {}".format(self.id) +
            "\n Name: {}".format(self.name) +
            "\n Sensor Frame Size: {}".format(self.sensor_frame_size) +
            "\n Sensor Data File: {}".format(self.sensor_data_file) +
            "\n}"
        )
    
    def raw_bytes_repr(self, byte: bytes) -> str:
        return "b'" + "".join(f"\\x{b:02x}" for b in byte) + "'"
        
    def get_formatted_poll_codes(self):
        to_return = []
        for byte, sensor in self.poll_codes.items():
            to_return.append("{} : {}".format(self.raw_bytes_repr(byte), sensor))
        
        return "\n".join(to_return)