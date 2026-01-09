from .toggle import Toggle
from BaseController import BaseSensor
from dataclasses import dataclass
from typing import List

@dataclass
class Feature:
    name: str
    value: Toggle
    sensors: List[BaseSensor]

    def bit(self):
        return "1" if self.value is Toggle.ENABLED else "0"