from .feature import Feature
from .toggle import Toggle
from dataclasses import dataclass
from typing import List

@dataclass
class Bitmask():
    features: List[Feature]

    def __str__(self):
        try:
            return "".join(feature.bit() for feature in reversed(self.features))
        except KeyError:
            return ""