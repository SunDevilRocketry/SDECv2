# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass

@dataclass(frozen=True)
class BaseSensor:
    short_name: str
    name: str
    size: int
    data_type: type
    unit: str

    def __str__(self):
        return (
            "Sensor:{" +
            f"\n Short Name: {self.short_name}" +
            f"\n Name: {self.name}" + 
            f"\n Size: {self.size}" + 
            f"\n Data Type: {self.data_type}" +
            f"\n Unit: {self.unit}" +
            "\n}"
        )
    
    def __repr__(self):
        return self.__str__()