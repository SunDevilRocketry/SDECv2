from .feature import Feature
from .preset_config import PresetConfig
from dataclasses import dataclass
from typing import Dict

@dataclass
class Preset:
    config_settings: PresetConfig
    # imu_offset: ImuOffset
    # baro_preset: BaroPreset
    # sero_preset: ServoPreset

    def __str__(self):
        return (
            "Preset:{" + 
            "\n Config Settings: {}".format(self.config_settings) +
            "\n}"
        )