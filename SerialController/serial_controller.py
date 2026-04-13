# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import serial
import serial.tools.list_ports

from .comport import Comport, Status
from typing import List
from SDECv2.BaseController import BaseController

class SerialObj:
    """
    Represents a serial connection object for communication with the Flight Computer.
    Provides methods to manage and interact with the serial port.
    """

    def __init__(self):
        self.comport: Comport
        self.serialObj: serial.Serial = serial.Serial()
        self.target: BaseController = None

    def available_comports(self) -> List[str]:
        """
        Get a list of available COM ports.

        Returns:
            List[str]: List of available COM port names.
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def init_comport(self, name: str, baudrate: int, timeout: int) -> Comport:
        """
        Initialize the COM port with the specified parameters.

        Args:
            name (str): Name of the COM port.
            baudrate (int): Baud rate for the connection.
            timeout (int): Timeout for the connection.

        Returns:
            Comport: Configured COM port instance.
        """
        self.comport = Comport(name, baudrate, timeout)
        self.serialObj.port = name
        self.serialObj.baudrate = baudrate
        self.serialObj.timeout = timeout
        return self.comport

    def open_comport(self) -> bool:
        """
        Open the initialized COM port.

        Returns:
            bool: True if the port was successfully opened, False otherwise.
        """
        if self.comport.status is Status.OPEN: return False 
        if self.serialObj.is_open: return False
        if not self.comport: return False

        self.serialObj.open()
        self.comport.status = Status.OPEN
        
        return True

    def close_comport(self) -> bool:
        """
        Close the currently open COM port.

        Returns:
            bool: True if the port was successfully closed, False otherwise.
        """
        if self.comport.status is Status.CLOSED: return False
        if not self.serialObj.is_open: return False
        if not self.comport: return False

        self.serialObj.close()
        self.comport.status = Status.CLOSED

        return True

    def send(self, bytes: bytes) -> None:
        """
        Send data over the serial connection.

        Args:
            bytes (bytes): Data to send.
        """
        try:
            self.serialObj.write(bytes)
        except serial.SerialException as e:
            print(f"Error: {e}")

    def read(self, num_bytes: int = 1) -> bytes:
        """
        Read data from the serial connection.

        Args:
            num_bytes (int): Number of bytes to read.

        Returns:
            bytes: Read data.
        """
        try:
            data = self.serialObj.read(size=num_bytes)
            return data
        except serial.SerialException as e:
            print(f"Error: {e}")
            return b""
        
    def reset_input_buffer(self) -> None:
        """
        Reset the input buffer of the serial port.

        Returns:
            None
        """
        try:
            self.serialObj.reset_input_buffer()
        except serial.SerialException as e:
            print(f"Error: {e}")

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
            f"{"  " * indent}Serial Obj {{\n" +
            f"{spaces}Port: {self.serialObj.port}\n" + 
            f"{spaces}Baud: {self.serialObj.baudrate}\n" +
            f"{spaces}Timeout: {self.serialObj.timeout}\n" +
            f"{"  " * indent}}}"
        )
    
    def __str__(self):
        """
        Return a string representation of the preset configuration.
        """
        return self.pretty_print()
    
    def __repr__(self):
        return self.__str__()