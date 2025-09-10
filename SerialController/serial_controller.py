from .comport import Comport

class SerialObj:
    def __init__(self):
        self.comport: Comport
        self.baudrate: int = 0
    
    def init_comport(self) -> Comport:
        self.comport = Comport()
        return self.comport

    def open_comport(self) -> bool:
        return self.comport.open()
    
    def close_comport(self) -> bool:
        return self.comport.close()

    def send_byte(self, byte: bytes) -> None:
        pass

    def send_bytes(self, bytes: bytearray) -> None:
        pass

    def read_byte(self) -> bytes:
        return bytes(1)
    
    def read_bytes(self) -> bytearray:
        return bytearray([1])
    
    def __str__(self):
        return (
                "SerialController:{" +
                "Comport: {}".format(self.comport) + " "
                "Baudrate: {}}}".format(self.baudrate)
            )
    
    def __repr__(self):
        return self.__str__()