from .bitmask import FeatureBitmask, DataBitmask
from .preset_config import PresetConfig
from dataclasses import dataclass, field

@dataclass
class Preset:
    enabled_features: FeatureBitmask
    enabled_data: DataBitmask
    config: PresetConfig
    size: int = field(init=False)

    def pretty_print(self, indent=0):
        spaces = " " * indent
        to_string = ("Preset:{\n" + 
            f"{spaces}Enabled Features: {self.enabled_features}\n" +
            f"{spaces}Enabled Data: {self.enabled_data}\n" +
            f"{spaces}Preset Config: \n{self.config.pretty_print(indent=2)}\n" +
            "}\n"
        )
        return to_string

    def __str__(self):
        return self.pretty_print()