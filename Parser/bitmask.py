# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import struct

from .data import Data
from .feature import Feature
from .toggle import Toggle
from dataclasses import dataclass, field
from typing import List

@dataclass
class FeatureBitmask():
    """
    Represents a bitmask for features, storing their binary representation.
    Provides methods to convert the bitmask to integer and bytes.
    """

    bitmask: str = ""
    features: List[Feature] = field(default_factory=list)

    def __str__(self):
        """
        Return the binary string representation of the feature bitmask.

        Returns:
            str: Binary string representation of the bitmask.
        """
        bits = "".join(feature.bit() for feature in reversed(self.features))
        return bits.zfill(8)
    
    def to_int(self) -> int:
        """
        Convert the feature bitmask to an integer.

        Returns:
            int: Integer representation of the bitmask.
        """
        return int(self.__str__(), 2)

    def to_bytes(self) -> bytes:
        """
        Convert the feature bitmask to bytes.

        Returns:
            bytes: Byte representation of the bitmask.
        """
        return struct.pack("<I", self.to_int())

@dataclass
class DataBitmask():
    """
    Represents a bitmask for data, storing their binary representation.
    Provides methods to convert the bitmask to integer and bytes.
    """

    bitmask: str = ""
    datas: List[Data] = field(default_factory=list)

    def __str__(self):
        """
        Return the binary string representation of the data bitmask.

        Returns:
            str: Binary string representation of the bitmask.
        """
        bits = "".join(data.bit() for data in reversed(self.datas))
        return bits.zfill(8)
    
    def to_int(self) -> int:
        """
        Convert the data bitmask to an integer.

        Returns:
            int: Integer representation of the bitmask.
        """
        return int(self.__str__(), 2)

    def to_bytes(self) -> bytes:
        """
        Convert the data bitmask to bytes.

        Returns:
            bytes: Byte representation of the bitmask.
        """
        return struct.pack("<I", self.to_int())