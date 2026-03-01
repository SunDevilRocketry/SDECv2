# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FlashSensorFrame:
    values: Dict[str, int | float] = field(default_factory=dict[str, int | float])