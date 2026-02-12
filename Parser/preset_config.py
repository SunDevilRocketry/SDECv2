import builtins

from .bitmask import FeatureBitmask, DataBitmask
from BaseController import BaseSensor
from dataclasses import dataclass, field
from enum import Enum
from typing import List

# Prest entries
@dataclass
class PresetDataBitmask:
    size: int = 4
    data_type: type = int

    def __str__(self):
        return "Data Bitmask"

@dataclass
class PresetFeatureBitmask:
    size: int = 4
    data_type: type = int

    def __str__(self):
        return "Feature Bitmask"

@dataclass
class PresetChecksum:
    size: int = 4
    data_type: type = int

    def __str__(self):
        return "Checksum"

@dataclass
class PresetEntry:
    name: str
    size: int
    data_type: type

    def __str__(self):
        return f"Name: {self.name} | Size: {self.size} | Data Type: {self.data_type}"

# Preset fields
@dataclass
class ConfigData:
    checksum: PresetChecksum
    feature_bitmask: PresetFeatureBitmask
    data_bitmask: PresetDataBitmask
    entries: list[PresetEntry]

    def pretty_print(self, indent=0):
        spaces = " " * indent
        entries_string = "\n".join(spaces + str(entry) for entry in self.entries)
        return (
            f"{spaces}Checksum\n" +
            f"{spaces}Feature Bitmask\n" +
            f"{spaces}Data Bitmask\n" +
            f"{entries_string}\n"
        )

    def __str__(self):
        return self.pretty_print()

@dataclass
class ImuPreset:
    entries: list[PresetEntry]

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

@dataclass
class BaroPreset:
    entries: list[PresetEntry]

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

@dataclass 
class ServoPreset:
    entries: list[PresetEntry]

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

# Final preset class
@dataclass
class PresetConfig:
    config_data: ConfigData
    imu_preset: ImuPreset
    baro_preset: BaroPreset
    servo_preset: ServoPreset

    def pretty_print(self, indent=0):
        spaces = " " * indent
        return (
            f"{spaces}Config Data: \n{self.config_data.pretty_print(3)}\n" +
            f"{spaces}IMU Preset: {self.imu_preset}\n" +
            f"{spaces}Baro Preset: {self.baro_preset}\n" +
            f"{spaces}Servo Preset: {self.servo_preset}\n"
        )

    def __str__(self):
        return self.pretty_print()