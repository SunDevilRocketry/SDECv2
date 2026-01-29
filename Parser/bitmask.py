from .data import Data
from .feature import Feature
from dataclasses import dataclass
from typing import List

@dataclass
class FeatureBitmask():
    features: List[Feature]

    def __str__(self):
        return "".join(feature.bit() for feature in reversed(self.features))

@dataclass
class DataBitmask():
    datas: List[Data]

    def __str__(self):
        return "".join(data.bit() for data in reversed(self.datas))