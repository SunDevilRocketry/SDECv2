from .feature import Feature
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Data:
    config_data: Dict[Feature, List[bytes]]