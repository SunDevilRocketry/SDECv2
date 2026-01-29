from .preset_config import PresetConfig
from dataclasses import dataclass, field

@dataclass
class Preset:
    config_settings: PresetConfig
    # config_data: ConfigData
    # imu_offset: ImuOffset
    # baro_preset: BaroPreset
    # sero_preset: ServoPreset
    size: int = field(init=False)

    def __str__(self):
        return (
            "Preset:{" + 
            "\n Config Settings: {}".format(self.config_settings) +
            "\n}"
        )