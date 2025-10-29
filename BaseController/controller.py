from .sensor import Sensor
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Controller:
    id: bytes
    name: str
    poll_codes: Dict[bytes, Sensor]
    sensor_frame_size: int
    sensor_data_file: str

    def __str__(self):
        return (
            "Controller:{" +
            "\n ID: {}".format(self.id) +
            "\n Name: {}".format(self.name) +
            "\n Sensor Frame Size: {}".format(self.sensor_frame_size) +
            "\n Sensor Data File: {}".format(self.sensor_data_file) +
            "\n}"
        )
    
    def get_formatted_poll_codes(self):
        to_return = []
        for byte, sensor in self.poll_codes.items():
            to_return += "{} : {}".format(byte, sensor)
        
        return "\n".join(to_return)