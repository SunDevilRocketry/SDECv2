# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass

@dataclass
class Firmware:
    """
    Represents firmware with metadata such as ID, name, and preset details (unused).
    Provides methods for string representation of the firmware.
    """

    id: bytes
    name: str
    preset_frame_size: int
    preset_file: str

    def __str__(self):
        """
        Return a string representation of the firmware.

        Returns:
            str: String representation of the firmware's attributes.
        """
        return (
            "Firmware:{" +
            f"\n ID: {self.id}" + 
            f"\n Name: {self.name}" +
            f"\n Preset Frame Size: {self.self.preset_frame_size}" +
            f"\n Preset File: {self.preset_file}" +
            "\n}"
        )