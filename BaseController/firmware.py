from dataclasses import dataclass

@dataclass
class Firmware:
    id: bytes
    name: str
    preset_frame_size: int
    preset_file: str