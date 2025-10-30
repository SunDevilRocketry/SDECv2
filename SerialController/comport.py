import serial

from enum import Enum

class Status(Enum):
    CLOSED = 0
    OPEN = 1

class Comport:
    def __init__(self, name: str, baudrate: int, timeout: int):
        self.name: str = name
        self.status: Status = Status.CLOSED
        self.baudrate: int = baudrate
        self.timeout: int = timeout

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
            "\n Name: {}".format(self.name) +
            "\n Status: {}".format(self.status) +
            "\n Baudrate: {}".format(self.baudrate) +
            "\n Timeout: {}".format(self.timeout) +
            "\n}"
        )
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name and self.status == other.status