import builtins

from .bitmask import Bitmask
from BaseController import BaseSensor
from dataclasses import dataclass
from typing import List

@dataclass
class PresetConfig():
    enabled_flags: Bitmask
    enabled_data: Bitmask
    sensors: List[BaseSensor]
    struct_format: str

    def __post_init__(self):
        for i, bit in enumerate(str(self.enabled_flags)):
            if bit == "0": continue

            feature = self.enabled_flags.features[i]

            for sensor in feature.sensors:
                self.sensors.append(sensor)

                match sensor.data_type:
                    case builtins.float:
                        self.struct_format += "f"
                    case builtins.int:
                        match sensor.size:
                            case 1: self.struct_format += "b"
                            case 2: self.struct_format += "h"
                            case 4: self.struct_format += "i"                