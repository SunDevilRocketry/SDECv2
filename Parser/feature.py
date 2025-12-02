from BaseController import BaseSensor

@dataclass
class Feature:
    
    name: str
    sensors: List[BaseSensor]
    
    
#bitmask string spits out 0 or 1
#do sensor_flags same as other