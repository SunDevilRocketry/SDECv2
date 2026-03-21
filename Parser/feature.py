# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .toggle import Toggle
from dataclasses import dataclass

@dataclass
class Feature:
    """
    Represents a feature with a name and toggle value.
    Provides methods to calculate its bit representation.
    """

    name: str
    value: Toggle

    def bit(self):
        """
        Get the binary representation of the feature's toggle value.

        Returns:
            str: "1" if enabled, "0" otherwise.
        """
        return "1" if self.value is Toggle.ENABLED else "0"