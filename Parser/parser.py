import builtins
import struct

from .bitmask import FeatureBitmask, DataBitmask
from .data import Data
from .flash_data import FlashData
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
        self.num_preset_frames = 0
        self.preset_frame_size = 0
        self.num_sensor_frames = 0
        self.sensor_frame_size = 0
        self.sensor_struct_format = ""
        self._compute_frames()

    def _compute_frames(self):
        enabled_data = self.preset.config_settings.enabled_data

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
    
    def download_preset(self) -> FlashData:
        return FlashData(
            data_name=""
        )
    
    def verify_preset(self) -> FlashData:
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

        enabled_data = self.preset.config_settings.enabled_data
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