# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

import serial

from .comport import Comport, Status

class SerialObj:
    def __init__(self):
        self.comport: Comport
        self.serialObj: serial.Serial = serial.Serial()
    
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
    
    def __str__(self):
        return (
                "SerialController:{" +
                "\n{}".format(self.comport) +
                "\n}"
            )
    
    def __repr__(self):
        return self.__str__()