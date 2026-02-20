# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import serial
import serial.tools.list_ports

from .comport import Comport, Status
from typing import List

class SerialObj:
    def __init__(self):
        self.comport: Comport
        self.serialObj: serial.Serial = serial.Serial()

    def available_comports(self) -> List[str]:
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def init_comport(self, name: str, baudrate: int, timeout: int) -> Comport:
        self.comport = Comport(name, baudrate, timeout)
        self.serialObj.port = name
        self.serialObj.baudrate = baudrate
        self.serialObj.timeout = timeout
        return self.comport

    def open_comport(self) -> bool:
        if self.comport.status is Status.OPEN: return False 
        if self.serialObj.is_open: return False
        if not self.comport: return False

        self.serialObj.open()
        self.comport.status = Status.OPEN
        
        return True

    def close_comport(self) -> bool:
        if self.comport.status is Status.CLOSED: return False
        if not self.serialObj.is_open: return False
        if not self.comport: return False

        self.serialObj.close()
        self.comport.status = Status.CLOSED

        return True

    def send(self, bytes: bytes) -> None:
        try:
            self.serialObj.write(bytes)
        except serial.SerialException as e:
            print(f"Error: {e}")

    def read(self, num_bytes: int = 1) -> bytes:
        try:
            data = self.serialObj.read(size=num_bytes)
            return data
        except serial.SerialException as e:
            print(f"Error: {e}")
            return b""
        
    def reset_input_buffer(self) -> None:
        try:
            self.serialObj.reset_input_buffer()
        except serial.SerialException as e:
            print(f"Error: {e}")
    
    def __str__(self):
        return (
                "SerialController:{" +
                "\n{}".format(self.comport) +
                "\n}"
            )
    
    def __repr__(self):
        return self.__str__()