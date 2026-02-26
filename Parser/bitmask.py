import struct

from .data import Data
from .feature import Feature
from .toggle import Toggle
from dataclasses import dataclass, field
from typing import List

@dataclass
class FeatureBitmask():
    bitmask: str = ""
    features: List[Feature] = field(default_factory=list)

    def __str__(self):
        bits = "".join(feature.bit() for feature in reversed(self.features))
        return bits.zfill(8)
    
    def to_int(self) -> int:
        return int(self.__str__(), 2)

    def to_bytes(self) -> bytes:
        return struct.pack("<I", self.to_int())

@dataclass
class DataBitmask():
    bitmask: str = ""
    datas: List[Data] = field(default_factory=list)

    def __str__(self):
        bits = "".join(data.bit() for data in reversed(self.datas))
        return bits.zfill(8)
    
    def to_int(self) -> int:
        return int(self.__str__(), 2)

    def to_bytes(self) -> bytes:
        return struct.pack("<I", self.to_int())