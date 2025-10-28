from BaseController import *
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Controller:
    id: bytes
    name: str
    poll_codes: Dict[bytes, Sensor]
    sensor_frame_size: int
    sensor_data_file: str