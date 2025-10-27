from .sensor import Sensor
from typing import List, Callable, Dict

class SensorSentry:
    def __init__(self):
        self.sensors: List[Sensor] = []

    def init_sensor(self, name: str, unit: str, convert_data: Callable[[float], float]) -> None:
        new_sensor = Sensor(name, unit, convert_data)
        self.sensors.append(new_sensor)

    def sensor_dump(self) -> Dict[Sensor, float]:
        sensor_dump = {}

        for sensor in self.sensors:
            sensor_dump[Sensor] = sensor.data_dump()

        return sensor_dump