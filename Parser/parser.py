from .data import Data
from .feature import Feature
from .preset import Preset
from typing import List

class Parser:
    def __init__(self, 
                 preset: Preset, 
                 data_bitmask: bytes, 
                 features: List[Feature], 
                 sensor_frame_size: int, 
                 num_frames: int):
        self.preset = preset
        self.data_bitmask = data_bitmask
        self.features = features
        self.sensor_frame_size = sensor_frame_size
        self.num_frames = num_frames
    
    def download_preset(self) -> Data:
        return Data({})
    
    def verify_preset(self) -> Data:
        return Data({})
    
    def upload_preset(self) -> Data:    
        return Data({})
    
    def flash_extract_parse(self) -> Data:
        return Data({})