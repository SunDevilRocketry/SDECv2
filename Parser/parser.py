import builtins
import json
import struct

from .bitmask import FeatureBitmask, DataBitmask
from .create_configs import appa_feature_bitmask_from_bits, appa_data_bitmask_from_bits
from .data import Data
from .flash_data import FlashData
from .feature import Feature
from .preset_config import PresetConfig, ConfigEntry
from .preset_data import PresetData, DataEntry
from .toggle import Toggle
from SerialController import SerialObj
from typing import List

FLASH_SIZE = 524288

class Parser:
    def __init__(self, preset_config: PresetConfig, preset_data: PresetData | None):
        self.preset_config = preset_config
        self.preset_data: PresetData | None = None

    @classmethod
    def from_file(cls, path: str) -> "Parser":
        with open(path, "r") as f:
            json_input = json.load(f)

        if json_input is None:
            raise ValueError("Error: No JSON found")

        feature_bitmask_json: str = json_input.get("Feature Bitmask")
        if feature_bitmask_json == "": raise ValueError("Error: No Feature Bitmask")

        data_bitmask_json: str = json_input.get("Data Bitmask")
        if data_bitmask_json == "": raise ValueError("Error: No Data Bitmask")

        config_data_json: list[dict] = json_input.get("Config Data", [])
        if config_data_json == []: raise ValueError("Error: No Config Data")

        imu_data_json: list[dict] = json_input.get("IMU Data", [])
        if imu_data_json == []: raise ValueError("Error: No IMU Data")

        baro_data_json: list[dict] = json_input.get("Baro Data", [])
        if baro_data_json == []: raise ValueError("Error: No Baro Data")

        servo_data_json: list[dict] = json_input.get("Servo Data", [])
        if servo_data_json == []: raise ValueError("Error: No Servo Data")

        def make_entries(entries: list[dict]):
            config_entries: list[ConfigEntry] = []
            data_entries: list[DataEntry] = []

            for entry in entries:
                name = str(entry.get("Name"))
                if name == "": raise ValueError("Error: No Entry name")

                size = entry.get("Size", 0)
                if size == 0: raise ValueError("Error: No Entry size")
                size = int(size)
                
                data_type = entry.get("Data Type")
                match data_type:
                    case "int": data_type = int
                    case "float": data_type = float
                    case _: raise ValueError("Error: No or invalid Entry data type") 
                
                value = entry.get("Value", 0)
                if value == 0: raise ValueError("Error: No Entry value")
                match data_type:
                    case builtins.int: value = int(value)
                    case builtins.float: value = float(value)
                    case _: raise ValueError("Error: Invalid Entry data type")
                
                config_entries.append(
                    ConfigEntry(
                        name=name,
                        size=size,
                        data_type=data_type
                    )
                )

                data_entries.append(
                    DataEntry(
                        name=name,
                        size=size,
                        data_type=data_type,
                        value=value
                    )
                )

            return config_entries, data_entries

        data_config, config_data = make_entries(config_data_json)
        imu_config, imu_data = make_entries(imu_data_json)
        baro_config, baro_data = make_entries(baro_data_json)
        servo_config, servo_data = make_entries(servo_data_json)

        preset_config = PresetConfig(
            data_config=data_config,
            imu_config=imu_config,
            baro_config=baro_config,
            servo_config=servo_config
        )

        preset_data = PresetData(
            feature_bitmask=appa_feature_bitmask_from_bits(feature_bitmask_json),
            data_bitmask=appa_data_bitmask_from_bits(data_bitmask_json),
            config_data=config_data,
            imu_data=imu_data,
            baro_data=baro_data,
            servo_data=servo_data
        )

        return cls(preset_config, preset_data)

    def reset(self):
        self.num_preset_frames = 0
        self.preset_frame_size = 0
        self.num_sensor_frames = 0
        self.sensor_frame_size = 0
        self.sensor_struct_format = ""
        self._compute_frames()

    def _compute_frames(self):
        enabled_data = self.preset.enabled_data

        sensor_count = 0
        for i, bit in enumerate(str(enabled_data)):
            if bit == "0": continue

            data = enabled_data.datas[i]
            for sensor in data.sensors:
                sensor_count += 1
                self.sensor_frame_size += sensor.size

                match sensor.data_type:
                    case builtins.float:
                        self.sensor_struct_format += "f"

                    case builtins.int:
                        match sensor.size:
                            case 1: self.sensor_struct_format += "b"
                            case 2: self.sensor_struct_format += "h"
                            case 4: self.sensor_struct_format += "i"  

                    case builtins.str:
                        self.sensor_struct_format += "c"

        self.preset_frame_size = self.sensor_frame_size
        while self.preset_frame_size < self.preset.size + 2: # TODO confirm + 2
            self.preset_frame_size += self.sensor_frame_size

    def _parse_preset(self, preset_bytes: bytes) -> PresetData:
        struct_format = self.preset_config.struct_format
        if struct.calcsize(struct_format) != len(preset_bytes): print("Error: Preset Config size does not match preset bytes")

        vals = struct.unpack(struct_format, preset_bytes)[0]

        checksum = vals[0]

        # Gets 8 least significant bits of 4 byte int as a string
        feature_bitmask = appa_feature_bitmask_from_bits(format(vals[1] & 0xFF, "08b"))
        data_bitmask = appa_data_bitmask_from_bits(format(vals[2] & 0xFF, "08b")) 

        vals = vals[3:]  
        def set_data_entries(vals_idx: int, config_entries: list[ConfigEntry]) -> list[DataEntry]:
            data_entries: list[DataEntry] = []
            
            for entry in config_entries:
                val = vals[vals_idx]
                data_entries.append(
                    DataEntry(
                        name=entry.name,
                        size=entry.size,
                        data_type=entry.data_type,
                        value=val
                    )
                )
                vals_idx += 1

            return data_entries
        
        config_data = set_data_entries(0, self.preset_config.data_config)
        vals_idx = len(config_data)
        
        imu_data = set_data_entries(vals_idx, self.preset_config.imu_config)
        vals_idx += len(imu_data)

        baro_data = set_data_entries(vals_idx, self.preset_config.baro_config)
        vals_idx += len(baro_data)

        servo_data = set_data_entries(vals_idx, self.preset_config.servo_config)

        preset_data = PresetData(
            feature_bitmask=feature_bitmask,
            data_bitmask=data_bitmask,
            config_data=config_data,
            imu_data=imu_data,
            baro_data=baro_data,
            servo_data=servo_data
        )

        if checksum != preset_data.checksum:
            print("Erorr: Received checksum does not match calculated checksum")

        return preset_data
    
    def download_preset(self) -> FlashData:
        # Set self.downloaded_preset
        return FlashData(
            data_name=""
        )
    
    def verify_preset(self) -> FlashData:        
        self.download_preset()
        # compare checksums 

        return FlashData(
            data_name=""
        )
    
    def upload_preset(self) -> FlashData:
        return FlashData(
            data_name=""
        )
    
    def flash_extract(self, serial_connection: SerialObj) -> List[FlashData]:
        all_flash_data: List[FlashData] = []
        # flash opcode
        serial_connection.send(b"\x22")
        # flash extract subcommand code
        serial_connection.send(b"\xC0")

        # extract the number of frames in bitmask from flash (4096 blocks max)
        # each frame reads the amount of bytes the size of the frame
        # add these to the overall bytes of flash
        num_frames = FLASH_SIZE // self.sensor_frame_size
        sensor_frame_bytes = bytearray(FLASH_SIZE)

        offset = 0
        for i in range(num_frames):
            if (i % 100 == 0): print(f"Reading block {i} ...")
            # TODO confirm if active roll requires 4 extra bytes
            chunk = serial_connection.read(self.sensor_frame_size)
            sensor_frame_bytes[offset:offset + self.sensor_frame_size] = chunk
            offset += self.sensor_frame_size

        # receive unused bytes amount of bytes
        serial_connection.read(FLASH_SIZE % self.sensor_frame_size)

        # receive status byte
        serial_connection.read()

        # get struct format from config preset

        # parse the bytes, using the presets struct format
        # verify the adding 2s
        preset_size = self.preset.size
        preset_bytes = sensor_frame_bytes[2:preset_size + 2]
        # TODO parse_preset()

        # calculate frame size and num preset frames from preset data bitmask
        # use the size of the preset data bitmask as the sensor frame size
        # num preset frames is how many preset frames fit in the data size???
        start_idx = self.num_preset_frames * self.sensor_frame_size
        stop_idx = start_idx + self.sensor_frame_size

        enabled_data = self.preset.enabled_data
        while stop_idx < FLASH_SIZE:
            curr_frame_bytes = sensor_frame_bytes[start_idx:stop_idx]
            curr_frame_values = struct.unpack(self.sensor_struct_format, curr_frame_bytes)
            # iterate through the values and put into Data objects
            value_idx = 0
            for i, bit in enumerate(str(enabled_data)):
                if bit == "0": continue

                data = enabled_data.datas[i]
                if data.bit == "0": continue

                flash_data = FlashData(data_name=data.name)
                for sensor in data.sensors:
                    flash_data.values[sensor] = curr_frame_values[value_idx]
                    value_idx += 1
                all_flash_data.append(flash_data)

            start_idx += self.sensor_frame_size
            stop_idx += self.sensor_frame_size

        return all_flash_data