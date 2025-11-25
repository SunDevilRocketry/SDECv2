import builtins
import struct

from typing import Callable

def bytes_to_float(raw_bytes: bytes) -> float:
    invalid_bytes = b"\xFF\xFF\xFF\xFF" # NaN check
    if raw_bytes == invalid_bytes: bytes = b"\x00\x00\x00\x00"

    return struct.unpack("f", raw_bytes)[0]

def bytes_to_int(bytes: bytes) -> int:
    return int.from_bytes(bytes, byteorder="little")

# Convert raw bytes to a float or int and use the conversion function
def process_data_bytes(data_bytes: bytes, 
                       data_type: type, 
                       convert_data: Callable[[float | int], float | int]
                       ) -> float | int | None:
    if not data_bytes:
        print("Failed to get data from board")
        return None

    match data_type:
        case builtins.float:
            data_number = bytes_to_float(data_bytes)
        case builtins.int:
            data_number = bytes_to_int(data_bytes)
        case _:
            data_number = None
    if data_number is None:
        print("Failed to convert bytes to number")
        return None

    converted_number = convert_data(data_number)
    if converted_number is None:
        print("Failed to convert number")
        return None

    return converted_number