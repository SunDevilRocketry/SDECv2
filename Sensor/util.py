# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

"""
This module provides functions to convert and process raw bytes to standard data types. 
"""

import builtins
import struct

from typing import Callable

from SDECv2.Exceptions import InvalidDataError

def bytes_to_float(raw_bytes: bytes) -> float:
    invalid_bytes = b"\xFF\xFF\xFF\xFF" # NaN check
    if raw_bytes == invalid_bytes: bytes = b"\x00\x00\x00\x00"

    return struct.unpack("f", raw_bytes)[0]

def bytes_to_int(bytes: bytes) -> int:
    return int.from_bytes(bytes, byteorder="little")

# Convert raw bytes to a float or int and use the conversion function
def process_data_bytes(data_bytes: bytes, 
                       data_type: type, 
                       convert_data: Callable[[float | int], float | int] | None
                       ) -> float | int | None:
    """
    Convert bytes to an int or float then use a conversion function if provided.

    Args:
        data_bytes (bytes): The data to convert from bytes in to an int or float.
        data_type (type): The data type the bytes need to be converted into.
        convert_data (Callable[[float | int], float | int] | None): The conversion function to process the int or float.

    Returns:
        float | int | None: The final data value.
    """
    if data_bytes is None: raise InvalidDataError("Failed to get data from board")

    match data_type:
        case builtins.float:
            data_number = bytes_to_float(data_bytes)
        case builtins.int:
            data_number = bytes_to_int(data_bytes)
        case builtins.str:
            return None
        case _:
            data_number = None
    if data_number is None: raise InvalidDataError("Failed to convert bytes to number")

    if convert_data is None: return data_number

    converted_number = convert_data(data_number)
    if converted_number is None: raise InvalidDataError("Failed to convert number")

    return converted_number