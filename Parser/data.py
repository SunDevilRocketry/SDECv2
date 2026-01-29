from .feature import Feature
from ..BaseController import BaseSensor
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Data:
    feature: Feature
    values: Dict[BaseSensor, int | float] = field(default_factory=Dict[BaseSensor, int | float])