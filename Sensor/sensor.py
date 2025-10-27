from typing import Callable

class Sensor:
    def __init__(self, name: str, unit: str, convert_data: Callable[[float], float]):
        self.name = name
        self.unit = unit
        self.convert_data = convert_data
        
    def data_dump(self) -> float:
        # TODO:
        # send command opcode
        # send sensor dump code
        # read a byte to get the size of sensor dump
        # for each byte in the size of sensor dump read and store byte from serial
        # parse through the read bytes to extract this sensor's data
        # format sensor readout 
        return 0

    def poll(self) -> None:
        pass