import builtins
import json
import struct

from .bitmask import FeatureBitmask, DataBitmask
from .data import Data
from .flash_sensor_frame import FlashSensorFrame
from .feature import Feature
from .preset import Preset
from .toggle import Toggle
from SerialController import SerialObj
from typing import List

FLASH_SIZE = 524288

class Parser:
    def __init__(self, preset: Preset):
        self.preset = preset
        self.preset.size = 88 # TODO preset will just calc this itself when its done
        self.reset()

    def reset(self):
        self.sensor_struct_format = ">"
        self._compute_frames()

    def _compute_frames(self):
        enabled_data = self.preset.config_settings.enabled_data

        for i, bit in enumerate(str(enabled_data)):
            if bit == "0": continue

            data = enabled_data.datas[i]
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
                        self.sensor_struct_format += "b"
    
    def download_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def verify_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def upload_preset(self) -> FlashSensorFrame:
        return FlashSensorFrame()
    
    def flash_extract(self, serial_connection: SerialObj, extract_to_file: bool) -> List[FlashSensorFrame]:
        # flash opcode
        serial_connection.send(b"\x22")
        # flash extract subcommand code
        serial_connection.send(b"\xC0")

        # extract the number of frames in bitmask from flash (4096 blocks max)
        # each frame reads the amount of bytes the size of the frame
        # add these to the overall bytes of flash
        # num_frames = FLASH_SIZE // self.sensor_frame_size
        # num_frames = math.ceil(FLASH_SIZE / 512)
        # print(f"Num frames: {num_frames}")
        # print(f"num_preset_frames: {self.num_preset_frames}")
        # print(f"preset_frame_size: {self.preset_frame_size}")
        # print(f"num_sensor_frames: {self.num_sensor_frames}")
        # print(f"sensor_frame_size: {self.sensor_frame_size}")

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

        # get struct format from config preset

        # parse the bytes, using the presets struct format
        preset_bytes = flash_bytes[2:self.preset.size + 2]
        # TODO parse_preset()
        # TODO this should create a parser object for use in the rest of flash extract
        
        print("preset bytes:")
        print(preset_bytes)
        print("*********")
        
        # calculate frame size and num preset frames from preset data bitmask
        # use the size of the preset data bitmask as the sensor frame size
        # num preset frames is how many preset frames fit in the data size???
        sensor_frame_names = []
        enabled_data = self.preset.config_settings.enabled_data
        for i, bit in enumerate(str(enabled_data)):
            if bit == "0": continue
            data = enabled_data.datas[i]
            for sensor in data.sensors: sensor_frame_names.append(sensor.name)
        
        sensor_frame_size = struct.calcsize(self.sensor_struct_format)
        print(f"Sensor Frame Size: {sensor_frame_size}")

        start_idx = self.preset.size + 2
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
                print("Two duplicate frames, likely reading cleared flash memory")
                break
            prev_frame_bytes = curr_frame_bytes
            print("--------------------")

        if extract_to_file:
            with open("output/flash_extract.json", "w") as f:
                json.dump(sensor_frame_dicts, f, indent=4)

        return all_sensor_frames