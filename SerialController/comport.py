from enum import Enum

class OPEN(Enum): pass
class CLOSED(Enum): pass

class Comport:
    def __init__(self):
        self.name = "Comport-One"
        self.status = CLOSED

    def open(self) -> bool:
        if self.status is CLOSED:
            self.status = OPEN
            return True
        else: return False

    def close(self) -> bool:
        if self.status is OPEN:
            self.status = CLOSED
            return True
        else:
            return False
        
    def __str__(self):
        return (
            "Comport:{" +
            "Name: {}".format(self.name) + " "
            "Status: {}}}".format(self.status)
        )
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name and self.status == other.status