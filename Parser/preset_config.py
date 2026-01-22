import builtins

from .bitmask import Bitmask
from BaseController import BaseSensor
from dataclasses import dataclass, field
from typing import List

@dataclass
class PresetConfig():
    enabled_flags: Bitmask
    enabled_data: Bitmask
    sensors: List[BaseSensor] = field(init=False)
    struct_format: str = ">"
    size: int = 0

    def __post_init__(self):
        self.sensors = []
        self.struct_format = ""

        for i, bit in enumerate(str(self.enabled_flags)):
            if bit == "0": continue

            feature = self.enabled_flags.features[i]

            for sensor in feature.sensors:
                self.sensors.append(sensor)
                self.size += sensor.size

                match sensor.data_type:
                    case builtins.float:
                        self.struct_format += "f"
                    case builtins.int:
                        match sensor.size:
                            case 1: self.struct_format += "b"
                            case 2: self.struct_format += "h"
                            case 4: self.struct_format += "i"  

    def __str__(self) -> str:
        return (
            "Preset Config:{" +
            "\n Enabled Flags Bitmask: {}".format(self.enabled_flags) +
            "\n Enabled Data Bitmask: {}".format(self.enabled_data) +
            "\n Sensors: {}".format(self.sensors) + 
            "\n Struct Format: {}".format(self.struct_format) +
            "\n}"
        )