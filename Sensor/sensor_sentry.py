import builtins

from .sensor import Sensor
from .util import bytes_to_float, bytes_to_int, process_data_bytes
from SerialController import SerialObj
from typing import List, Callable, Dict, Optional

class SensorSentry:
    def __init__(self, sensors: Optional[List[Sensor]] = None):
        self.sensors: List[Sensor] = sensors if sensors is not None else []
        self.size: int = sum(sensor.size for sensor in self.sensors)

    def init_sensor(
            self, 
            short_name: str, 
            name: str, 
            size: int, 
            data_type: type, 
            unit: str, 
            convert_data: Callable[[float | int], float | int], 
            poll_code: bytes, 
            offset: int):
        new_sensor = Sensor(short_name, name, size, data_type, unit, convert_data, poll_code, offset)
        self.sensors.append(new_sensor)
        self.size += size

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)
        self.size += sensor.size

    def sensor_dump(self, serial_connection: SerialObj) -> Dict[Sensor, float | int | None]:
        # Sensor opcode 
        serial_connection.send(b"\x03")

        # Dump subcommand code
        serial_connection.send(b"\x01")

        # Get size of sensor dump from Flight Computer
        sensor_dump_size = serial_connection.read()
        sensor_dump_size = int.from_bytes(sensor_dump_size, "big")

        # Get sensor dump but only the minimum required amount for the sensors in the sentry
        last_sensor = self.sensors[-1]
        data_bytes = serial_connection.read(last_sensor.offset + last_sensor.size)

        # Extract each sensor's data from the sensor dump
        sensor_dump = {}
        for sensor in self.sensors:
            # Read and convert raw bytes to the readout
            sensor_data_bytes = data_bytes[sensor.offset:sensor.offset+sensor.size]
            converted_number = process_data_bytes(sensor_data_bytes, sensor.data_type, sensor.convert_data)
            sensor_dump[sensor] = converted_number

        return sensor_dump