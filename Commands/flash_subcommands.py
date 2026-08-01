# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from SDECv2.SerialController import SerialObj

def flash_read(serial_connection: SerialObj, address: bytes, num_bytes: int, file: str):
    #---------------DELETE BEFORE PULL-------------------------
    #3 options -------
    '-a Specify a memory address to read from', #format 0xXXXXXX (SDECv1), convert to int, to bytes?
    '-n Specify a number of bytes to read from flash memory', #int from 1 to 31 (SDECv1)
    '-f Specify a file to use for output data', 
    # options, like flash extract, should be handled by the CLI, and passed as arguments
    # to the function.

    #Order of Operations -----------
    #X -- done, not checked
    #V -- done, checked

    #send flash OPCODE X
    #send read subcommand code X
    #send base address to read from X
    #read num_bytes bytes from buffer and combine into list X
    #verify flash read X (taken directly from sdec hw_commands.py)
    #display bytes on terminal X
    #if -f used, save bytes of specified file (in a_output?)
    #-------------------------------

    #---------------DELETE BEFORE PULL-------------------------

    """
    Reads bytes from the flash chip.

    Args:
        serial_connection (SerialObj): Serial Connection to the Flight Computer.
        address (byte): base memory address to read from.
        num_bytes (int): number of bytes to be read.
        file (str): name of file bytes to be output to.

    Returns:
        

    Raises:
        
    """


    #flash opcode
    serial_connection.send(b"\x22")
    #flash read subcommand code
    serial_connection.send(num_bytes.to_bytes(1,byteorder="big",signed=False))
    #send base address
    serial_connection.send(address)
    #read bytes
    data = serial_connection.read(num_bytes)
    #verify flash read
    flash_read_status = serial_connection.read()
    if flash_read_status != b'\x00':
        print('Error: Flash Read Unsuccessful')
    #print bytes to terminal
    for byte in data:
        print()

def flash_write(serial_connection: SerialObj, address: bytes, message: bytes | str, file: str):
    # to do ---------------------------------
    '-b Specify a byte to write to flash memory'  
    '-s Specify a string to write to flash memory'
    '-a Specify a memory address to write to'     
    '-f Specify a file to use for input data'     
    #check if flash write is enabled(?) and enable if not (dont think this is needed)
    #send flash opcode X
    #calculate and send flash write subcommand opcode X
    #send base address
    #send byte to flash
    #check return code for verification
    # to do ---------------------------------
    #send flash opcode
    serial_connection.send(b"\x22")
    #calculate and send flash write subcommand opcode
    num_bytes = len(message)
    flash_write_opcode = num_bytes+96
    serial_connection.send(flash_write_opcode.to_bytes(1,byteorder="big",signed=False))
    #send base address
    serial_connection.send(address)
    #send byte to flash
    serial_connection.send(message)
    #chekc return code for verification
    return_code = serial_connection.read()
    if (return_code == b""):
         print("Error: No Response Code Received")
    elif(return_code == b"\x00"):
         print("Flash Write Successful")
    else:
         print("Error: Unrecognized Response Code Received")

def flash_enable(serial_connection: SerialObj):

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

def flash_disable(serial_connection: SerialObj):
    
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