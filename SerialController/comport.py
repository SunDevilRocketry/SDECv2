# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import serial

from enum import Enum

class Status(Enum):
    CLOSED = 0
    OPEN = 1

class Comport:
    """
    Represents a serial connection object for communication with the Flight Computer.
    Provides methods to manage and interact with the serial port.
    """

    def __init__(self, name: str, baudrate: int, timeout: int):
        """
        Initialize the COM port with the specified parameters.

        Args:
            name (str): Name of the COM port.
            baudrate (int): Baud rate for the connection.
            timeout (int): Timeout for the connection.

        """
        self.name: str = name
        self.status: Status = Status.CLOSED
        self.baudrate: int = baudrate
        self.timeout: int = timeout

    def open(self) -> bool:
        """
        Open a Comport.

        Returns:
            bool: True if the Comport successfully opens, False otherwise.
        """
        if self.status is Status.CLOSED:
            self.status = Status.OPEN
            return True
        else: 
            return False

    def close(self) -> bool:
        """
        Close an open Comport.

        Returns:
            bool: True if the Comport successfully closes, False otherwise.
        """
        if self.status is Status.OPEN:
            self.status = Status.CLOSED
            return True
        else:
            return False
        
    def __str__(self):
        """
        Return a string representation of the Comport.

        Returns:
            str: String representation of the Comport's attributes.
        """
        return (
            "Comport:{" +
            "\n Name: {}".format(self.name) +
            "\n Status: {}".format(self.status) +
            "\n Baudrate: {}".format(self.baudrate) +
            "\n Timeout: {}".format(self.timeout) +
            "\n}"
        )
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        """
        Return a comparison of two Comports.

        Returns:
            bool: True if the attributes are equal, False otherwise.
        """
        return self.name == other.name and self.status == other.status