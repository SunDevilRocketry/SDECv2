# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass

@dataclass(frozen=True)
class BaseSensor:
    """
    Represents a base sensor with metadata name, size, data type, unit.
    Provides methods for string representation of the sensor.
    """

    short_name: str
    name: str
    size: int
    data_type: type
    unit: str

    def __str__(self):
        """
        Return a string representation of the sensor.

        Returns:
            str: String representation of the sensor's attributes.
        """
        return (
            "Sensor:{" +
            "\n Short Name: {}".format(self.short_name) +
            "\n Name: {}".format(self.name) + 
            "\n Size: {}".format(self.size) + 
            "\n Data Type: {}".format(self.data_type) +
            "\n Unit: {}".format(self.unit) +
            "\n}"
        )
    
    def __repr__(self):
        return self.__str__()