from BaseController import BaseSensor
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FlashData:
    data_name: str
    values: Dict[BaseSensor, int | float] = field(default_factory=dict[BaseSensor, int | float])