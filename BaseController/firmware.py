from dataclasses import dataclass

@dataclass
class Firmware:
    id: bytes
    name: str
    preset_frame_size: int
    preset_file: str

    def __str__(self):
        return (
            "Firmware:{" +
            "\n ID: {}".format(self.id) + 
            "\n Name: {}".format(self.name) +
            "\n Preset Frame Size: {}".format(self.preset_frame_size) +
            "\n Preset File: {}".format(self.preset_file) +
            "\n}"
        )