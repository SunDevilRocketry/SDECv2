# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .toggle import Toggle
from dataclasses import dataclass
from SDECv2.BaseController import BaseSensor
from typing import List

@dataclass
class Data:
    name: str
    value: Toggle
    sensors: List[BaseSensor]
    size: int = 0

    def bit(self):
        return "1" if self.value is Toggle.ENABLED else "0"
    
    def __post_init__(self):
        if self.size is None:
            for sensor in self.sensors: self.size += sensor.size