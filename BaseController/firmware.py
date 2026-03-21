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
            "\n ID: {}".format(self.id) + 
            "\n Name: {}".format(self.name) +
            "\n Preset Frame Size: {}".format(self.preset_frame_size) +
            "\n Preset File: {}".format(self.preset_file) +
            "\n}"
        )