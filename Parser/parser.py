import builtins
import json
import struct

from .bitmask import FeatureBitmask, DataBitmask
from .create_configs import appa_feature_bitmask_from_bits, appa_data_bitmask_from_bits
from .data import Data
from .flash_sensor_frame import FlashSensorFrame
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

        self.sensor_struct_format = ">"

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

    def _compute_frames(self, bits: str):
        enabled_data = appa_data_bitmask_from_bits(bits)

        datas_idx = 0
        for i, bit in enumerate(str(enabled_data)):
            if bit == "0": continue

            data = enabled_data.datas[datas_idx]
            for sensor in data.sensors:
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

            datas_idx += 1

    def _parse_preset(self, preset_bytes: bytes) -> PresetData:
        struct_format = self.preset_config.struct_format
        if struct.calcsize(struct_format) != len(preset_bytes): print("Error: Preset Config size does not match preset bytes")

        vals = struct.unpack(struct_format, preset_bytes)

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

        self.preset_data = preset_data # TODO maybe remove
        return preset_data
    
    def download_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def verify_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def upload_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def flash_extract(self, serial_connection: SerialObj, store_preset: bool, store_data: bool) -> List[FlashSensorFrame]:
        # flash opcode
        serial_connection.send(b"\x22")
        # flash extract subcommand code
        serial_connection.send(b"\xC0")

        num_frames = FLASH_SIZE // 512
        print(f"Num frames: {num_frames}")

        flash_bytes = bytearray()
        for i in range(num_frames):
            if (i % 128 == 0): print(f"Reading block {i} ...")
            chunk = serial_connection.read(num_bytes=512)
            
            num_received = len(chunk)
            if num_received == 0: 
                print(f"[{i + 1}/{num_frames}] Timeout: Flash is empty")
            elif num_received != 512:
                print(f"[{i + 1}/{num_frames}] Timeout: Partial read of length {num_received}")

            flash_bytes.extend(chunk)

        print(f"{len(flash_bytes)} bytes received from flash")
        if len(flash_bytes) == FLASH_SIZE: print("Max flash bytes received")

        # receive status byte
        serial_connection.read()

        preset_size = struct.calcsize(self.preset_config.struct_format)
        preset_bytes = flash_bytes[2:preset_size + 2]
        
        self._parse_preset(preset_bytes)
        
        if self.preset_data is None: raise ValueError("Erorr: Failed to parse preset")

        if store_preset: self.preset_data.save_preset()
            
        self._compute_frames(str(self.preset_data.data_bitmask))

        sensor_frame_names = []
        enabled_data = appa_data_bitmask_from_bits(str(self.preset_data.data_bitmask))
        
        data_idx = 0
        for bit in str(enabled_data):
            if bit == "0": continue
            data = enabled_data.datas[data_idx]
            for sensor in data.sensors: sensor_frame_names.append(sensor.name)
            data_idx += 1
        
        sensor_frame_size = struct.calcsize(self.sensor_struct_format)
        print(f"Sensor Frame Size: {sensor_frame_size}")

        start_idx = preset_size + 2
        stop_idx = start_idx + sensor_frame_size

        print(f"Initial start_idx: {start_idx}")
        print(f"Initial stop_idx: {stop_idx}")
        
        all_sensor_frames: List[FlashSensorFrame] = []
        sensor_frame_dicts = []
        prev_frame_bytes = bytearray(512)
        while stop_idx < FLASH_SIZE:
            curr_frame_bytes = flash_bytes[start_idx:stop_idx]
            print(curr_frame_bytes)

            curr_frame_values = struct.unpack(self.sensor_struct_format, curr_frame_bytes)
            curr_sensor_frame = {}
            for name, value in zip(sensor_frame_names, curr_frame_values):
                curr_sensor_frame[name] = value
                print(f"{name} : {value}")
            
            start_idx += sensor_frame_size
            stop_idx += sensor_frame_size

            all_sensor_frames.append(FlashSensorFrame(curr_sensor_frame))
            sensor_frame_dicts.append(curr_sensor_frame)

            if prev_frame_bytes == curr_frame_bytes: 
                print("Two duplicate frames, likely reading cleared flash memory, breaking")
                break
            prev_frame_bytes = curr_frame_bytes
            print("--------------------")

        if store_data:
            with open("a_output/flash_extract.json", "w") as f:
                json.dump(sensor_frame_dicts, f, indent=4)

        return all_sensor_frames