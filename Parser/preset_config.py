# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import builtins
from dataclasses import dataclass, field

@dataclass
class ConfigEntry:
    """
    Represents a configuration entry with metadata name, size, and data type.
    Provides methods for string representation.
    """

    name: str
    size: int
    data_type: type

    def __str__(self):
        """
        Return a string representation of the configuration entry.

        Returns:
            str: String representation of the entry's attributes.
        """
        spaces = " " * (22 - len(self.name))
        return f"Name: {self.name} {spaces} | Size: {self.size} | Data Type: {self.data_type}"

@dataclass
class PresetConfig:
    """
    Represents the configuration for a preset, including data, IMU, barometric, and servo configurations.
    Provides methods for pretty-printing and structure formatting.
    """

    data_config: list[ConfigEntry]
    lora_config: list[ConfigEntry]
    imu_config: list[ConfigEntry]
    baro_config: list[ConfigEntry]
    servo_config: list[ConfigEntry]

    struct_format: str = field(default="<", init=False)

    def pretty_print(self, indent=0):
        """
        Return a formatted string representation of the preset configuration.

        Args:
            indent (int): Indentation level for formatting.

        Returns:
            str: Formatted string representation of the preset configuration.
        """
        spaces = "  " * (1 + indent)
        return (
            "Preset Config {\n" +
            f"{spaces}Config Data: \n{"\n".join(spaces + "  " + str(entry) for entry in self.data_config)}\n" +
            f"{spaces}LoRA Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.lora_config)}\n" +
            f"{spaces}IMU Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.imu_config)}\n" +
            f"{spaces}Baro Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.baro_config)}\n" +
            f"{spaces}Servo Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.servo_config)}\n"
            "}"
        )

    def __str__(self):
        """
        Return a string representation of the preset configuration.
        """
        return self.pretty_print()
    
    def get_entry_struct_format(self, entries: list[ConfigEntry]) -> str:
        """
        Return a formatted string representation of an entry list.

        Args:
            entries (list[ConfigEntry]): A list of preset config entries that make up one Entry into the Config.

        Returns:
            str: Formatted string representation of the entire config entry list.
        """
        struct_format = ""
        for entry in entries:
            match entry.data_type:
                case builtins.float: 
                    struct_format += "f"
                case builtins.int:
                    match entry.size:
                        case 1: struct_format += "B"
                        case 2: struct_format += "H"
                        case 4: struct_format += "I"

        return struct_format
    
    def __post_init__(self):
        """
        Initialize the structure format string based on the configuration entries.
        """
        self.struct_format += "I" # Checksum
        self.struct_format += "I" # Feature Bitmask
        self.struct_format += "I" # Data Bitmask 

        self.struct_format += self.get_entry_struct_format(self.data_config)
        self.struct_format += self.get_entry_struct_format(self.lora_config)
        self.struct_format += self.get_entry_struct_format(self.imu_config)
        self.struct_format += self.get_entry_struct_format(self.baro_config)
        self.struct_format += self.get_entry_struct_format(self.servo_config)