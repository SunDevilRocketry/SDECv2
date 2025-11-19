import struct

def bytes_to_float(raw_bytes) -> float:
    invalid_bytes = b"\xFF\xFF\xFF\xFF" # NaN check
    if raw_bytes == invalid_bytes: bytes = b"\x00\x00\x00\x00"

    return struct.unpack("f", raw_bytes)[0]

def bytes_to_int(bytes) -> int:
    return int.from_bytes(bytes, byteorder="little")