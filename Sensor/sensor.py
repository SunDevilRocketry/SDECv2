# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import serial
import time

from typing import Callable, Generator

from .util import bytes_to_float, bytes_to_int, process_data_bytes
from SDECv2.BaseController import BaseSensor
from SDECv2.SerialController import SerialObj
from SDECv2.Exceptions import SerialError

class Sensor(BaseSensor):
    """
    Represents a sensor with metadata and conversion functions.
    Provides methods for equality checks and string representation.
    """

    def __init__(
            self, 
            short_name: str, 
            name: str, 
            size: int, 
            data_type: type, 
            unit: str, 
            convert_data: Callable[[float | int], float | int,] | None, 
            poll_code: bytes, 
            offset: int
            ):
        super().__init__(short_name, name, size, data_type, unit)
        self.convert_data = convert_data
        self.poll_code = poll_code
        self.offset = offset

    # NOTE: Currently unsupported by v2.6.0 of Flight Computer Firmware
    def poll(self, 
                  serial_connection: SerialObj, 
                  timeout: int | None=None, 
                  count: int | None=None
                  ) -> Generator[float | int, None, None]:
        """
        Poll the sensor and yield the converted data.

        Args:
            serial_connection (SerialObj): The serial connection object.
            timeout (int | None): The maximum time to wait for a response.
            count (int | None): The number of times to poll.

        Yields:
            float | int: The converted sensor data.
        """
        # Sensor opcode
        serial_connection.send(b"\x03") 

        # Poll subcommand code
        serial_connection.send(b"\x02")

        # Tell the controller how many sensors to use
        num_sensors = 1
        serial_connection.send(num_sensors.to_bytes(1, "big"))

        # Send the current sensor poll code
        serial_connection.send(self.poll_code)

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
            converted_number = process_data_bytes(data_bytes, self.data_type, self.convert_data)
            if converted_number is not None: yield converted_number

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
            time.sleep(0.1)
            # Resume poll code
            serial_connection.send(b"\xEF")

    # NOTE: Currently unsupported by v2.6.0 of Flight Computer Firmware
    def dump(self, serial_connection: SerialObj) -> float | int:
        """
        Dump the sensor data.

        Args:
            serial_connection (SerialObj): The serial connection object.

        Returns:
            float | int: The converted sensor data.
        """
        # Sensor opcode
        serial_connection.send(b"\x03") 

        # Poll subcommand code
        serial_connection.send(b"\x02")

        # Tell the controller how many sensors to use
        num_sensors = 1
        serial_connection.send(num_sensors.to_bytes(1, "big"))

        # Send the current sensor poll code
        serial_connection.send(self.poll_code)

        # Start poll code
        serial_connection.send(b"\xF3")

        # Request poll code
        serial_connection.send(b"\x51")

        # Read and convert the sensor bytes
        data_bytes = serial_connection.read(num_bytes=self.size)
        converted_number = process_data_bytes(data_bytes, self.data_type, self.convert_data)
        
        # Stop poll code
        serial_connection.send(b"\x74")

        if converted_number is not None: return converted_number

        return 0
    
    def __eq__(self, other):
        """
        Check if two sensors are equal based on their attributes.

        Args:
            other (Sensor): The sensor to compare with.

        Returns:
            bool: True if sensors are equal, False otherwise.
        """
        if not isinstance(other, Sensor):
            return False
        
        return (self.short_name, self.poll_code, self.offset) == (other.short_name, other.poll_code, other.offset)
    
    def __hash__(self):
        """
        Compute a hash value for the sensor based on its attributes.
        Only hashes the unchanging attributes of the sensor. 

        Returns:
            int: Hash value of the sensor.
        """
        return hash((self.short_name, self.poll_code, self.offset))
    
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
            f"{"  " * indent}Sensor {{\n" +
            f"{spaces} Short Name: {self.short_name}\n" +
            f"{spaces} Name: {self.name}\n" + 
            f"{spaces} Size: {self.size}\n" + 
            f"{spaces} Data Type: {self.data_type}\n" +
            f"{spaces} Unit: {self.unit}\n" +
            f"{spaces} Poll Code: {self.poll_code}\n" +
            f"{spaces} Offset: {self.offset}\n" +
            f"{"  " * indent}}}"
        )

    
    def __str__(self):
        """
        Return a string representation of the sensor.

        Returns:
            str: String representation of the sensor's attributes.
        """
        return self.pretty_print()