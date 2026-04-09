# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import builtins
import json
import os
import pandas as pd
import struct

from .bitmask import FeatureBitmask, DataBitmask
from .create_configs import appa_feature_bitmask_from_bits, appa_data_bitmask_from_bits
from .data import Data
from .flash_sensor_frame import FlashSensorFrame
from .feature import Feature
from .preset_config import PresetConfig, ConfigEntry
from .preset_data import PresetData, DataEntry
from .toggle import Toggle
from SDECv2.SerialController import SerialObj
from typing import List
from SDECv2.Exceptions import SDECError
from SDECv2.Exceptions import InvalidDataError 
from SDECv2.Exceptions import MissingDataError
from SDECv2.Exceptions import ParserError

FLASH_SIZE = 524288

class Parser:
    """
    Parses and manages preset configurations and data for the Flight Computer.
    Provides methods to load, verify, upload, and manipulate presets.
    """

    def __init__(self, preset_config: PresetConfig, preset_data: PresetData | None):
        """
        Initialize the parser with preset configuration and data.

        Args:
            preset_config (PresetConfig): Configuration details for the preset.
            preset_data (PresetData | None): Data associated with the preset.
        """
        self.preset_config = preset_config
        self.preset_data = preset_data

        self.sensor_struct_format = "<bbI" # save bit, FC state, time since launch

    @classmethod
    def from_file(cls, path: str) -> "Parser":
        """
        Create a Parser instance from a JSON file.

        Args:
            path (str): Path to the JSON file containing preset data.

        Returns:
            Parser: A new Parser instance initialized with the file's data.

        Raises:
            ValueError: If required fields are missing or invalid in the JSON file.
        """
        with open(path, "r") as f:
            json_input = json.load(f)

        if json_input is None:
            raise FileNotFoundError("Error: No JSON found")

        feature_bitmask_json: dict = json_input.get("Feature Bitmask", {})
        if feature_bitmask_json == {}: raise MissingDataError("Error: No Feature Bitmask")

        data_bitmask_json: dict = json_input.get("Data Bitmask", {})
        if data_bitmask_json == {}: raise MissingDataError("Error: No Data Bitmask")

        config_data_json: list[dict] = json_input.get("Config Data", [])
        if config_data_json == []: raise MissingDataError("Error: No Config Data")

        imu_data_json: list[dict] = json_input.get("IMU Data", [])
        if imu_data_json == []: raise MissingDataError("Error: No IMU Data")

        baro_data_json: list[dict] = json_input.get("Baro Data", [])
        if baro_data_json == []: raise MissingDataError("Error: No Baro Data")

        servo_data_json: list[dict] = json_input.get("Servo Data", [])
        if servo_data_json == []: raise MissingDataError("Error: No Servo Data") 

        def make_entries(entries: list[dict]):
            config_entries: list[ConfigEntry] = []
            data_entries: list[DataEntry] = []

            for entry in entries:
                name = str(entry.get("Name"))
                if name == "": raise InvalidDataError("Error: No Entry name") 

                size = entry.get("Size", 0)
                if size == 0: raise InvalidDataError("Error: No Entry size") 
                size = int(size)
                
                data_type = entry.get("Data Type")
                match data_type:
                    case "int": data_type = int
                    case "float": data_type = float
                    case _: raise InvalidDataError("Error: No or invalid Entry data type")  
                
                value = entry.get("Value", "")
                if value == "": raise InvalidDataError("Error: No Entry value") 
                match data_type:
                    case builtins.int: value = int(value)
                    case builtins.float: value = float(value)
                    case _: raise InvalidDataError("Error: Invalid Entry data type")
                
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
        
        feature_bitmask = ""
        for val in feature_bitmask_json.values():
            bit = "1" if val else "0"
            feature_bitmask = bit + feature_bitmask
        feature_bitmask = "0" * (8 - len(feature_bitmask)) + feature_bitmask 

        data_bitmask = ""
        for val in data_bitmask_json.values():
            bit = "1" if val else "0"
            data_bitmask = bit + data_bitmask
        data_bitmask = "0" * (8 - len(data_bitmask)) + data_bitmask

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
            feature_bitmask=appa_feature_bitmask_from_bits(feature_bitmask),
            data_bitmask=appa_data_bitmask_from_bits(data_bitmask),
            config_data=config_data,
            imu_data=imu_data,
            baro_data=baro_data,
            servo_data=servo_data
        )

        return cls(preset_config, preset_data)

    def _compute_frames(self, bits: str) -> None:
        """
        Compute the sensor frame structure based on the data bitmask.

        Args:
            bits (str): Binary string representing the data bitmask.
        """
        enabled_data = appa_data_bitmask_from_bits(bits)

        datas_idx = 0
        for bit in str(enabled_data):
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
        """
        Parse preset data from raw bytes.

        Args:
            preset_bytes (bytes): Raw bytes representing the preset data.

        Returns:
            PresetData: Parsed preset data object.

        Raises:
            ValueError: If the preset data is invalid or incomplete.
        """
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
            checksum_print = 'b"' + ''.join(f'\\x{b:02X}' for b in struct.pack(b"<I", checksum)) + '"'
            calculated_print = 'b"' + ''.join(f'\\x{b:02X}' for b in struct.pack(b"<I", preset_data.checksum)) + '"'

            print(f"Warning: Received checksum {checksum_print} does not match calculated checksum {calculated_print}")

        return preset_data
    
    def download_preset(self, serial_connection: SerialObj, path="a_output/downloaded_preset.json") -> None:
        """
        Download the preset from the Flight Computer and save it to a file.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.
            path (str): Path to save the downloaded preset JSON file.
        """
        # preset opcode
        serial_connection.send(b"\x24")
        # download subcommand code
        serial_connection.send(b"\x02")

        preset_len = struct.calcsize(self.preset_config.struct_format)

        preset_bytes = serial_connection.read(preset_len)

        preset_data = self._parse_preset(preset_bytes)

        preset_data.save_preset(path)
    
    def verify_preset(self, serial_connection: SerialObj) -> bool:
        """
        Verify the checksum of the preset on the Flight Computer.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.

        Returns:
            bool: True if the checksum is valid, False otherwise.
        """
        # preset opcode
        serial_connection.send(b"\x24")
        # verify subcommand code
        serial_connection.send(b"\x03")

        received_checksum = serial_connection.read()

        match received_checksum:
            case b"\x00":
                print("Invalid Checksum")
                return False
            case b"\x01":
                print("Valid Checksum")
                return True
            case _:
                print("Unexpected Result")
                return False
    
    @classmethod
    def upload_preset(cls, serial_connection: SerialObj, path: str="a_input/appa_preset.json") -> "Parser":
        """
        Upload a preset to the Flight Computer from a JSON file.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.
            path (str): Path to the JSON file containing the preset data.

        Returns:
            Parser: A Parser instance initialized with the uploaded preset data.

        Raises:
            ValueError: If the preset data is invalid or the file does not exist.
        """
        if not os.path.exists(path): print(f"File {path} does not exist")

        parser = Parser.from_file(path=path)
 
        if parser.preset_data is None: 
            raise ParserError("Error: Failed to create preset data from file")
        
        data = parser.preset_data.to_bytes()

        # preset opcode
        serial_connection.send(b"\x24")
        # upload subcommand code
        serial_connection.send(b"\x01")
 
        serial_connection.send(data)

        return parser
    
    def flash_extract(self, serial_connection: SerialObj, preset_path: str="a_output/flash_extracted_preset.json", data_path: str="a_output/flash_extract.csv") -> List[FlashSensorFrame]:
        """
        Extract flash memory data from the Flight Computer.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.
            preset_path (str): Path to save the extracted preset JSON file.
            data_path (str): Path to save the extracted sensor data as a CSV file.

        Returns:
            List[FlashSensorFrame]: List of sensor frames extracted from flash memory.

        Raises:
            ValueError: If the preset data cannot be parsed.
        """
        # flash opcode
        serial_connection.send(b"\x22")
        # flash extract subcommand code
        serial_connection.send(b"\xC0")

        num_frames = FLASH_SIZE // 512

        flash_bytes = bytearray()
        for i in range(num_frames):
            if (i % 100 == 0): print(f"Reading block (size 512) {i} ...")
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
        
        flash_extract_preset = self._parse_preset(preset_bytes)
        
        if flash_extract_preset is None: raise ParserError("Erorr: Failed to parse preset")

        if preset_path != "": flash_extract_preset.save_preset(path=preset_path)
            
        self._compute_frames(str(flash_extract_preset.data_bitmask))

        sensor_frame_names = []
        enabled_data = appa_data_bitmask_from_bits(str(flash_extract_preset.data_bitmask))
        
        data_idx = 0
        for bit in str(enabled_data):
            if bit == "0": continue
            data = enabled_data.datas[data_idx]
            for sensor in data.sensors: sensor_frame_names.append(sensor.name)
            data_idx += 1
        
        sensor_frame_size = struct.calcsize(self.sensor_struct_format)

        # Calculate the start index based on how many sensor frames are needed for the preset 
        start_idx = sensor_frame_size
        while start_idx < preset_size: start_idx += sensor_frame_size
        stop_idx = start_idx + sensor_frame_size
        
        all_sensor_frames: List[FlashSensorFrame] = []
        sensor_frame_dicts = []
        while stop_idx < FLASH_SIZE:
            curr_frame_bytes = flash_bytes[start_idx:stop_idx]

            curr_frame_values = struct.unpack(self.sensor_struct_format, curr_frame_bytes)

            # Parse save bit, flight computer state, and time (set parts of a sensor frame)
            save_bit = curr_frame_values[0]
            fc_state = curr_frame_values[1]
            time = curr_frame_values[2] / 1_000

            curr_frame_values = curr_frame_values[3:]

            curr_sensor_frame = {"Save Bit": save_bit, "FC State": fc_state, "Time": time}
            for name, value in zip(sensor_frame_names, curr_frame_values):
                curr_sensor_frame[name] = value
            
            start_idx += sensor_frame_size
            stop_idx += sensor_frame_size

            all_sensor_frames.append(FlashSensorFrame(curr_sensor_frame))
            sensor_frame_dicts.append(curr_sensor_frame)

        if data_path != "":
            flash_data = pd.DataFrame(sensor_frame_dicts)
            flash_data.to_csv(data_path, index=False)

        return all_sensor_frames