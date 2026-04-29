# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import math
import time
import serial

from typing import List, Callable, Dict, Optional, Generator

from .create_sensors import rev2_dashboard_dump_sensors
from .sensor import Sensor
from .util import bytes_to_float, bytes_to_int, process_data_bytes
from SDECv2.SerialController import SerialObj
from SDECv2.Exceptions import SerialError

class SensorSentry:
    """
    Manages a collection of sensors and provides methods for initialization and polling.
    """

    def __init__(self, sensors: Optional[List[Sensor]] = None):
        """
        Initialize the SensorSentry with an optional list of sensors.

        Args:
            sensors (Optional[List[Sensor]]): List of sensors to manage.
        """
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
        """
        Initialize and add a new sensor to the sentry.

        Args:
            short_name (str): Short name of the sensor.
            name (str): Full name of the sensor.
            size (int): Size of the sensor data.
            data_type (type): Data type of the sensor.
            unit (str): Unit of measurement for the sensor.
            convert_data (Callable[[float | int], float | int]): Conversion function for sensor data.
            poll_code (bytes): Poll code for the sensor.
            offset (int): Offset for the sensor data.
        """
        new_sensor = Sensor(short_name, name, size, data_type, unit, convert_data, poll_code, offset)
        self.sensors.append(new_sensor)
        self.size += size

    def add_sensor(self, sensor: Sensor):
        """
        Add an existing sensor to the sentry.

        Args:
            sensor (Sensor): The sensor to add.
        """
        self.sensors.append(sensor)
        self.size += sensor.size

    # NOTE: Currently unsupported by v2.6.0 of Flight Computer Firmware
    def poll(self, 
             serial_connection: SerialObj,
             timeout: int | None=None,
             count: int | None=None
             ) -> Generator[Dict[Sensor, float | int | None], None, None]:
        """
        Poll the sensors and yield their data.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.
            timeout (int | None): Timeout for polling.
            count (int | None): Number of polls to perform.

        Yields:
            Generator[Dict[Sensor, float | int | None], None, None]: Sensor data for each poll.
        """
        # Verify sentry has configured sensors
        if len(self.sensors) == 0: 
            print("Sentry has no sensors")
            return None
        
        # Sensor opcode
        serial_connection.send(b"\x03")

        # Poll subcommand code 
        serial_connection.send(b"\x02")

        # Tell the controller how many sensors to use 
        num_sensors = len(self.sensors)
        serial_connection.send(num_sensors.to_bytes(1, "big"))

        # Send all the sensor poll codes
        for sensor in self.sensors:
            serial_connection.send(sensor.poll_code)

        # Start poll code 
        serial_connection.send(b"\xF3")

        # Polling loop
        start = time.time()
        poll_count = 0
        while timeout or count:
            # Request poll code
            serial_connection.send(b"\x51")

            # Read and convert the sensor bytes
            data_bytes = serial_connection.read(self.size)
            sensor_poll = {}
            offset = 0
            for sensor in self.sensors:
                sensor_data_bytes = data_bytes[offset:offset + sensor.size]
                converted_number = process_data_bytes(sensor_data_bytes, sensor.data_type, sensor.convert_data)
                sensor_poll[sensor] = converted_number
                offset += sensor.size
            
            yield sensor_poll

            poll_count += 1

            if timeout and time.time() - start >= timeout:
                # Stop poll code
                serial_connection.send(b"\x74")
                return

            if count and poll_count >= count:
                # Stop poll code
                serial_connection.send(b"\x74")
                return

            # Wait poll code
            serial_connection.send(b"\x44") 
            time.sleep(0.2)
            # Resume poll code
            serial_connection.send(b"\xEF")

    def dump(self, serial_connection: SerialObj) -> Dict[Sensor, float | int | None]:
        """
        Dump the sensor data.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.

        Returns:
            Dict[Sensor, float | int | None]: Sensor data.
        """
        # Verify sentry has configured sensors
        if len(self.sensors) == 0: 
            print("Sentry has no sensors")
            return {}
        
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

    @classmethod
    def dashboard_dump(cls, serial_connection: SerialObj) -> Dict[Sensor, float | int | None]:
        """
        Dashboard dump opcode.

        Args:
            serial_connection (SerialObj): Serial connection to the Flight Computer.

        Returns:
            Dict[Sensor, float | int | None]: Sensor data.
        """
        # Dashboard dump opcode
        serial_connection.send(b"\x30")

        # Avoid creating a serial_sentry to reduce overhead
        sensors = rev2_dashboard_dump_sensors()
        sensors_size = sum(sensor.size for sensor in sensors)

        data_bytes = serial_connection.read(sensors_size)

        sensor_dump = {}
        for sensor in sensors:
            # Read and convert raw bytes to the readout
            sensor_data_bytes = data_bytes[sensor.offset:sensor.offset+sensor.size]
            converted_number = process_data_bytes(sensor_data_bytes, sensor.data_type, sensor.convert_data)
            
            # Convert Python inf and NaN into JSON readable values
            if converted_number is not None:
                if math.isinf(converted_number): 
                    converted_number = 999999
                elif math.isnan(converted_number):
                    converted_number = None

            sensor_dump[sensor] = converted_number

        return sensor_dump
    
    def pretty_print(self, indent=0):
        """
        Return a formatted string representation of the preset configuration.

        Args:
            indent (int): Indentation level for formatting.

        Returns:
            str: Formatted string representation of the preset configuration.
        """
        spaces = "  " * (1 + indent)
        return (
            "Sensory Sentry {\n" +
            f"{spaces}Sensors: \n{"\n".join(sensor.pretty_print(1) for sensor in self.sensors)}\n" +
            f"{spaces}Size: {self.size}\n" +
            "}"
        )

    def __str__(self):
        """
        Return a string representation of the preset configuration.
        """
        return self.pretty_print()