# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .toggle import Toggle
from dataclasses import dataclass
from SDECv2.BaseController import BaseSensor
from typing import List

@dataclass
class Data:
    """
    Represents a data entry with associated sensors and metadata.
    Provides methods to calculate its bit representation.
    """

    name: str
    value: Toggle
    sensors: List[BaseSensor]
    size: int = 0

    def bit(self):
        """
        Get the binary representation of the data's toggle value.

        Returns:
            str: "1" if enabled, "0" otherwise.
        """
        return "1" if self.value is Toggle.ENABLED else "0"
    
    def __post_init__(self):
        """
        Calculate the total size of the data based on its sensors.
        """
        if self.size is None:
            for sensor in self.sensors: self.size += sensor.size