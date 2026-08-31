# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from SDECv2.SerialController import SerialObj

def flash_read(serial_connection: SerialObj, address: bytes, num_bytes_input: int, file: str | None = None):
    """
    Reads bytes from the flash chip.

    Args:
        serial_connection (SerialObj): Serial Connection to the Flight Computer.
        address (bytes): base memory address to read from.
        num_bytes_input (int): number of bytes to be read.
        file (str): name of file bytes to be output to.

    Returns:
        
    
    Raises:
        
    """


    #flash opcode
    serial_connection.send(b"\x22")
    #flash read subcommand code
    serial_connection.send(num_bytes_input.to_bytes(1,byteorder="big",signed=False))
    #send base address
    serial_connection.send(address)
    #read bytes
    data = serial_connection.read(num_bytes = num_bytes_input)
    #verify flash read
    flash_read_status = serial_connection.read()
    if flash_read_status != b'\x00':
        print('Error: Flash Read Unsuccessful')
    #print bytes to terminal
    for byte in data:
         print()
    print(data,flash_read_status)

def flash_write(serial_connection: SerialObj, address: bytes, message: bytes | str, file: str | None = None):
    """
    Writes bytes to the flash chip.

    Args:
        serial_connection (SerialObj): Serial Connection to the Flight Computer.
        address (bytes): base memory address to write to.
        message (bytes): bytes to be written to the flash chip.
        file (str): name of file bytes to be output to.

    Returns:
        
    Raises:
        
    """
        
    #send flash opcode
    serial_connection.send(b"\x22")
    #calculate and send flash write subcommand opcode
    num_bytes_input = len(message)
    flash_write_opcode = num_bytes_input+96
    serial_connection.send(flash_write_opcode.to_bytes(1,byteorder="big",signed=False))
    #send base address
    serial_connection.send(address)
    #send byte to flash
    serial_connection.send(message)
    #chekc return code for verification
    return_code = serial_connection.read(num_bytes = num_bytes_input)
    if (return_code == b""):
         print("Error: No Response Code Received")
    elif(return_code == b"\x00"):
         print("Flash Write Successful")
    else:
         print("Error: Unrecognized Response Code Received")
    print(num_bytes_input,return_code,address,message)

def flash_enable(serial_connection: SerialObj):
    """
    Enables writing to the flash chip.

    Args:
        serial_connection (SerialObj): Serial Connection to the Flight Computer.

    Returns:
        
    Raises:
        
    """
    #send flash opcode
    serial_connection.send(b"\x22")
    #send enable subcommand opcode
    serial_connection.send(b"\x20")
    #verify return code
    return_code = serial_connection.read()
    if (return_code == b""):
          print("Error: No Response Code Received")
    elif(return_code == b"\x00"):
          print("Flash Write Enabled Successfully")
    else:
          print("Error: Unknown Response Code Received")
          print(return_code)

def flash_disable(serial_connection: SerialObj):
    """
    Enables writing to the flash chip.

    Args:
        serial_connection (SerialObj): Serial Connection to the Flight Computer.

    Returns:
        
    Raises:
        
    """
    #send flash opcode
    serial_connection.send(b"\x22")
    #send enable subcommand opcode
    serial_connection.send(b"\x40")
    #verify return code
    return_code = serial_connection.read()
    if (return_code == b""):
          print("Error: No Response Code Received")
    elif(return_code == b"\x00"):
          print("Flash Write Disabled Successfully")
    else:
          print("Error: Unknown Response Code Received")
          print(return_code)