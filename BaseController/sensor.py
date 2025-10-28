from dataclasses import dataclass

@dataclass
class Sensor:
    short_name: str
    name: str
    size: int
    data_type: type
    units: str