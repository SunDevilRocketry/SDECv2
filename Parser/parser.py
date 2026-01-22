import struct

from .bitmask import Bitmask
from .data import Data
from .feature import Feature
from .preset import Preset
from SerialController import SerialObj
from typing import List

FLASH_SIZE = 524288

class Parser:
    def __init__(self, 
                 preset: Preset, 
                 data_bitmask: Bitmask, 
                 features: List[Feature], 
                 sensor_frame_size: int, 
                 num_frames: int):
        self.preset = preset
        self.data_bitmask = data_bitmask
        self.features = features
        self.sensor_frame_size = sensor_frame_size
        self.num_frames = num_frames
    
    def download_preset(self) -> Data:
        pass
    
    def verify_preset(self) -> Data:
        pass
    
    def upload_preset(self) -> Data:    
        pass
    
    def flash_extract(self, serial_connection: SerialObj) -> List[Data]:
        flash_data: List[Data] = []
        # flash opcode
        serial_connection.send(b"\x22")
        # flash extract subcommand code
        serial_connection.send(b"\xC0")
        # flush buffer ?
        # start timer ?

        # extract the number of frames in bitmask from flash (4096 blocks max)
        # each frame reads the amount of bytes the size of the frame
        # add these to the overall bytes of flash
        sensor_frame_bytes = b""
        for i in range(self.num_frames):
            if (i % 100 == 0): print(f"Reading block {i} ...")
            # if active roll read an extra 4??? do this better?
            sensor_frame_bytes += serial_connection.read(self.sensor_frame_size)

        # receive unused bytes amount of bytes
        serial_connection.read(FLASH_SIZE % self.sensor_frame_size)

        # receive status byte from engine controller (flight computer?)
        serial_connection.read()

        # get struct format from config preset
        struct_format = self.preset.config_settings.struct_format

        # parse the bytes, using the presets struct format
        # verify the adding 2s
        preset_size = self.preset.config_settings.size
        preset_bytes = sensor_frame_bytes[2:preset_size + 2]
        preset_values = struct.unpack(struct_format, preset_bytes)
        # iterate through the values and put into Data objects
        features = self.preset.config_settings.enabled_flags.features
        value_idx = 0
        for feature in features:
            feature_data = Data(feature=feature)
            for sensor in feature.sensors:
                feature_data.values[sensor] = preset_values[value_idx]
                value_idx += 1
            flash_data.append(feature_data)

        # calculate frame size and num preset frames from preset data bitmask
        # use the size of the preset data bitmask as the sensor frame size
        # num preset frames is how many preset frames fit in the data size???
        num_preset_frames = preset_size // self.sensor_frame_size + 1
        start_idx = num_preset_frames * self.sensor_frame_size
        stop_idx = start_idx + self.sensor_frame_size

        while stop_idx < FLASH_SIZE:
            curr_frame_bytes = sensor_frame_bytes[start_idx:stop_idx]
            curr_frame_values = struct.unpack(struct_format, curr_frame_bytes)
            # iterate through the values and put into Data objects
            value_idx = 0
            for feature in features:
                feature_data = Data(feature=feature)
                for sensor in feature.sensors:
                    feature_data.values[sensor] = curr_frame_values[value_idx]
                    value_idx += 1
                flash_data.append(feature_data)

        return flash_data