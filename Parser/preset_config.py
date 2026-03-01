# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import builtins
from dataclasses import dataclass

@dataclass
class ConfigEntry:
    name: str
    size: int
    data_type: type

    def __str__(self):
        spaces = " " * (22 - len(self.name))
        return f"Name: {self.name} {spaces} | Size: {self.size} | Data Type: {self.data_type}"

@dataclass
class PresetConfig:
    data_config: list[ConfigEntry]
    imu_config: list[ConfigEntry]
    baro_config: list[ConfigEntry]
    servo_config: list[ConfigEntry]

    struct_format: str = "<"

    def pretty_print(self, indent=0):
        spaces = "  " * (1 + indent)
        return (
            "Preset Config {\n" +
            f"{spaces}Config Data: \n{"\n".join(spaces + "  " + str(entry) for entry in self.data_config)}\n" +
            f"{spaces}IMU Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.imu_config)}\n" +
            f"{spaces}Baro Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.baro_config)}\n" +
            f"{spaces}Servo Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.servo_config)}\n"
            "}"
        )

    def __str__(self):
        return self.pretty_print()
    
    def __post_init__(self):
        self.struct_format += "I" # Checksum
        self.struct_format += "I" # Feature Bitmask
        self.struct_format += "I" # Data Bitmask 

        def add_entries(entries: list[ConfigEntry]):
            for entry in entries:
                match entry.data_type:
                    case builtins.float: 
                        self.struct_format += "f"
                    case builtins.int:
                        match entry.size:
                            case 1: self.struct_format += "B"
                            case 2: self.struct_format += "H"
                            case 4: self.struct_format += "I"
                
        add_entries(self.data_config)
        add_entries(self.imu_config)
        add_entries(self.baro_config)
        add_entries(self.servo_config)