import builtins

from .bitmask import FeatureBitmask, DataBitmask
from BaseController import BaseSensor
from dataclasses import dataclass, field
from typing import List

@dataclass
class PresetConfig():
    enabled_features: FeatureBitmask
    enabled_data: DataBitmask

    def __str__(self) -> str:
        return (
            "Preset Config:{" +
            "\n Enabled Features Bitmask: {}".format(self.enabled_features) +
            "\n Enabled Data Bitmask: {}".format(self.enabled_data) +
            "\n}"
        )