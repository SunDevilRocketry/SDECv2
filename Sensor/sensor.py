import builtins

from .util import bytes_to_float, bytes_to_int
from BaseController import BaseSensor
from typing import Callable

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

    def data_dump(self, serial_connection) -> float | int:
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
        if data_bytes:
            match self.data_type:
                case builtins.float:
                    data_number = bytes_to_float(data_bytes)
                case builtins.int:
                    data_number = bytes_to_int(data_bytes)
                case _:
                    data_number = None

            if data_number:
                converted_number = self.convert_data(data_number)
                if converted_number:
                    # Stop poll code
                    serial_connection.send(b"\x74")

                    return converted_number
                else:
                    print("Failed to convert number")
            else:
                print("Failed to convert bytes to number")
        else:
            print("Failed to get data from board")

        # Stop poll code
        serial_connection.send(b"\x74")

        return 0