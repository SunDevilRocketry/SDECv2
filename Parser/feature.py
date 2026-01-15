from .toggle import Toggle
from BaseController import BaseSensor
from dataclasses import dataclass
from typing import List

@dataclass
class Feature:
    name: str
    value: Toggle
    sensors: List[BaseSensor]
    size: int = 0

    def bit(self):
        return "1" if self.value is Toggle.ENABLED else "0"
    
    def __post_init__(self):
        if self.size is None:
            for sensor in self.sensors: self.size += sensor.size