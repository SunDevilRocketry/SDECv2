import serial

from enum import Enum

class Status(Enum):
    CLOSED = 0
    OPEN = 1

class Comport:
    def __init__(self, name, baudrate, timeout):
        self.name = name
        self.status = Status.CLOSED
        self.baudrate = baudrate
        self.timeout = timeout

    def open(self) -> bool:
        if self.status is Status.CLOSED:
            self.status = Status.OPEN
            return True
        else: return False

    def close(self) -> bool:
        if self.status is Status.OPEN:
            self.status = Status.CLOSED
            return True
        else:
            return False
        
    def __str__(self):
        return (
            "Comport:{" +
            "Name: {}".format(self.name) +
            "Status: {}".format(self.status) +
            "Baudrate: {}".format(self.baudrate) +
            "Timeout: {}}}".format(self.timeout)
        )
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name and self.status == other.status