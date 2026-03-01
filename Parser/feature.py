# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .toggle import Toggle
from dataclasses import dataclass

@dataclass
class Feature:
    name: str
    value: Toggle

    def bit(self):
        return "1" if self.value is Toggle.ENABLED else "0"