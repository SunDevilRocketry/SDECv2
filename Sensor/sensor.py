from BaseController import BaseSensor
from typing import Callable

import time

class Sensor(BaseSensor):
    def __init__(
            self, 
            short_name: str, 
            name: str, 
            size: int, 
            data_type: type, 
            unit: str, 
            convert_data: Callable[[float | int], float | int,], 
            poll_code: bytes, 
            offset: int
            ):

        super().__init__(short_name, name, size, data_type, unit)
        self.convert_data: Callable[[float | int], float | int] = convert_data
        self.poll_code: bytes = poll_code
        self.offset: int = offset
        self.opcode: bytes = opcode
    
    # def convert_data( self ) -> float:
    #     return self.convert_data()
    #     #refactor serial obj 

    def data_dump( self, subcommand, serialObj ) -> float:
        # TODO:
        #check appa.py for list of sensors, substring for dump
        #check hardwarecommand lines 341, 571,
        #commands for opcode
        
        #set command opcode
        #opcode = b'\x03'
        
        #send command opcode
        serialObj.send_byte( self.opcode )
        
        #send sensor poll subcommand code b'\x02' for all sensors
        serialObj.send_byte( subcommand )

        # Tell the controller how many sensors to use
        num_sensors = 1
        serialObj.send_byte( num_sensors.to_bytes( 1, 'big' ) )

        # Send the controller the sensor codes
        sensor_poll_code = self.opcode
        serialObj.send_byte( sensor_poll_code )

        # Start the sensor poll sequence
        serialObj.send_byte( b'\xF3' ) # START

        time.sleep(1)

        serialObj.send_byte(b'\x51') # REQUEST

        # read
        sensor_bytes_list = serialObj.read_bytes(self.size)

        # self.data_type 
        # convert from bytes to float
        # convert from bytes to int

        # use conversion function to convert data to sensor readout 

        serialObj.send_byte(b'\x51') # STOP



        
        
        #toal byte size of sensors is 28 bytes
        #sensor_dump_size_bytes = 28
        sensor_dump_size_bytes = serialObj.read_byte()
        sensor_dump_size_bytes = int.from_bytes(sensor_dump_size_bytes, "big")
        
        #intiliaze array to hold sensor dump bytes
        sensor_bytes_list = [] #should this be passed as a parameter?
        

        
         #sensor readout goes from bytes to int to unit integer
        
        #append bytes to byte list
        for i in range(sensor_dump_size_bytes):
            sensor_bytes_list.append( serialObj.read_byte() )    
            
        
        data_bytes = sensor_bytes_list[ self.offset : self.offset + self.size ]
        
        #still need to format
        
        
        # send command opcode
        # send sensor dump code
        # read a byte to get the size of sensor dump
        # for each byte in the size of sensor dump read and store byte from serial
        # parse through the read bytes to extract this sensor's data
        # format sensor readout 
        return 0

    def poll(self) -> None:
        pass
    
    