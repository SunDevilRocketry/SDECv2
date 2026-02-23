import builtins
import json
import struct
import zlib
from .bitmask import FeatureBitmask, DataBitmask
from dataclasses import dataclass, field

@dataclass
class DataEntry:
    name: str
    size: int
    data_type: type
    value: int | float | None = None

    def __str__(self):
        spaces = " " * (22 - len(self.name))
        return f"Name: {self.name} {spaces} | Size: {self.size} | Data Type: {self.data_type}"

@dataclass
class PresetData:
    feature_bitmask: FeatureBitmask
    data_bitmask: DataBitmask
    config_data: list[DataEntry]
    imu_data: list[DataEntry]
    baro_data: list[DataEntry]
    servo_data: list[DataEntry]

    checksum: int = field(init=False)

    def pretty_print(self, indent=0):
        spaces = "  " * indent
        return (
            f"{spaces}Feature Bitmask: {self.feature_bitmask}\n" + 
            f"{spaces}Data Bitmask: {self.data_bitmask}\n" +
            f"{spaces}Config Data: \n{"\n".join(spaces + "  " + str(entry) for entry in self.config_data)}\n" +
            f"{spaces}IMU Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.imu_data)}\n" +
            f"{spaces}Baro Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.baro_data)}\n" +
            f"{spaces}Servo Preset: \n{"\n".join(spaces + "  " + str(entry) for entry in self.servo_data)}\n"
        )

    def __str__(self):
        return self.pretty_print()

    def __post_init__(self):
        payload = bytearray()

        payload.extend(self.feature_bitmask.to_bytes())
        payload.extend(self.data_bitmask.to_bytes())

        def add_entries(entries: list[DataEntry]):
            for entry in entries:
                match entry.data_type:
                    case builtins.float: 
                        payload.extend(struct.pack("<f", entry.value))
                    case builtins.int:
                        match entry.size:
                            case 1: payload.extend(struct.pack("<b", entry.value))
                            case 2: payload.extend(struct.pack("<h", entry.value))
                            case 4: payload.extend(struct.pack("<i", entry.value))
                
        add_entries(self.config_data)
        add_entries(self.imu_data)
        add_entries(self.baro_data)
        add_entries(self.servo_data)

        object.__setattr__(self, "checksum", zlib.crc32(payload) & 0xFFFFFFFF)

    def save_preset(self, path: str="a_input/appa_preset.json") -> None:
        feature_bitmask = {}
        for feature in self.feature_bitmask.features:
            feature_bitmask[feature.name] = True if feature.bit() == "1" else False

        data_bitmask = {}
        for data in self.data_bitmask.datas:
            data_bitmask[data.name] = True if data.bit() == "1" else False
        
        def format_entry(entry: DataEntry):
            return {
                "Name": entry.name,
                "Size": entry.size,
                "Data Type": "int" if entry.data_type is builtins.int else "float",
                "Value": entry.value
            }

        json_output = {
            "Feature Bitmask": feature_bitmask,
            "Data Bitmask": data_bitmask,
            "Config Data": [format_entry(entry) for entry in self.config_data],
            "IMU Data": [format_entry(entry) for entry in self.imu_data],
            "Baro Data": [format_entry(entry) for entry in self.baro_data],
            "Servo Data": [format_entry(entry) for entry in self.servo_data]
        }

        with open(path, "w") as f:
            json.dump(json_output, f, indent=4)

    def to_bytes(self) -> bytes:
        data = bytearray()

        data.extend(struct.pack("<I", self.checksum))
        data.extend(struct.pack("<i", self.feature_bitmask.to_int()))
        data.extend(struct.pack("<i", self.data_bitmask.to_int()))

        def entries_to_bytes(entries: list[DataEntry]):
            for entry in entries:
                match entry.data_type:
                    case builtins.float:
                        data.extend(struct.pack("<f", entry.value))
                    case builtins.int:
                        match entry.size:
                            case 1: data.extend(struct.pack("<b", entry.value))
                            case 2: data.extend(struct.pack("<h", entry.value))
                            case 4: data.extend(struct.pack("<i", entry.value))

        entries_to_bytes(self.config_data)
        entries_to_bytes(self.imu_data)
        entries_to_bytes(self.baro_data)
        entries_to_bytes(self.servo_data)

        return data