# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .base_sensor import BaseSensor
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Controller:
    """
    Represents a controller with associated sensors and configuration.
    Provides methods for string representation and formatted poll codes.
    """

    id: bytes
    name: str
    poll_codes: Dict[bytes, BaseSensor]
    sensor_frame_size: int
    sensor_data_file: str

    def __str__(self):
        """
        Return a string representation of the controller.

        Returns:
            str: String representation of the controller's attributes.
        """
        return (
            "Controller:{" +
            f"\n ID: {self.id}" +
            f"\n Name: {self.name}" +
            f"\n Sensor Frame Size: {self.sensor_frame_size}" +
            f"\n Sensor Data File: {self.sensor_data_file}" +
            "\n}"
        )
    
    def raw_bytes_repr(self, byte: bytes) -> str:
        """
        Convert raw bytes to a formatted string representation.
        Useful for printing bytes received over serial and preventing Python from printing their ASCII representations.

        Args:
            byte (bytes): Raw bytes to format.

        Returns:
            str: Formatted string representation of the bytes.
        """
        return "b'" + "".join(f"\\x{b:02x}" for b in byte) + "'"
        
    def get_formatted_poll_codes(self):
        """
        Get a formatted string of poll codes and their associated sensors.

        Returns:
            str: Formatted string of poll codes and sensors.
        """
        to_return = []
        for byte, sensor in self.poll_codes.items():
            to_return.append(f"{self.raw_bytes_repr(byte)} : {sensor}")
        
        return "\n".join(to_return)