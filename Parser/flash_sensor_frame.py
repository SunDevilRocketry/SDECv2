# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FlashSensorFrame:
    """
    Represents a frame of sensor data with associated values.
    """

    def __init__(self, values: Dict[str, int | float]):
        """
        Initialize the FlashSensorFrame with sensor values.

        Args:
            values (Dict[str, int | float]): Dictionary of sensor names and their values.
        """
        self.values = values

    values: Dict[str, int | float] = field(default_factory=dict[str, int | float])