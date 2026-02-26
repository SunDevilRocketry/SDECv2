# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import builtins
import time

from .util import bytes_to_float, bytes_to_int, process_data_bytes
from BaseController import BaseSensor
from SerialController import SerialObj
from typing import Callable, Generator

class Sensor(BaseSensor):
    def __init__(
            self, 
            short_name: str, 
            name: str, 
            size: int, 
            data_type: type, 
            unit: str, 
            convert_data: Callable[[float | int], float | int,], 
            poll_code: bytes, 
            offset: int
            ):
        super().__init__(short_name, name, size, data_type, unit)
        self.convert_data: Callable[[float | int], float | int] = convert_data
        self.poll_code: bytes = poll_code
        self.offset: int = offset

    def __eq__(self, other):
        if not isinstance(other, Sensor):
            return False
        
        return (self.short_name, self.poll_code, self.offset) == (other.short_name, other.poll_code, other.offset)
    
    def __hash__(self):
        return hash((self.short_name, self.poll_code, self.offset))

    def poll(self, 
                  serial_connection: SerialObj, 
                  timeout: int | None=None, 
                  count: int | None=None
                  ) -> Generator[float | int, None, None]:
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

    def dump(self, serial_connection: SerialObj) -> float | int:
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