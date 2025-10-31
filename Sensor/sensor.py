from typing import Callable

class Sensor:
    def __init__( self, name: str, unit: str, convert_data: Callable[[float], float,], low_byte_range : int, upp_byte_range : int) :
        self.name = name
        self.unit = unit
        self.convert_data = convert_data
        self.low_byte_range = low_byte_range
        self.upp_byte_range = upp_byte_range
    
    def convert_data( self ) -> float:
        return self.conv_data
        
    def data_dump( self, opcode, subcommand ) -> float:
        # TODO:
        #check appa.py for list of sensors, substring for dump
        #check hardwarecommand lines 341, 571,
        #commands for opcode
        
        #set command opcode
        #opcode = b'\x03'
        
        #send command opcode
        serialObj.sendByte( opcode )
        
        #send sensor dump subcommand code b'\x01' for all sensors
        serialObj.sendByte( subcommand )
        
        
        #toal byte size of sensors is 28 bytes
        #sensor_dump_size_bytes = 28
        sensor_dump_size_bytes = serialObj.readByte()
        sensor_dump_size_bytes = int.from_bytes(sensor_dump_size_bytes, "big")
        
        #intiliaze array to hold sensor dump bytes
        sensor_bytes_list = [] #should this be passed as a parameter?
        

        
         #sensor readout goes from bytes to int to unit integer
        
        #append bytes to byte list
        for i in range(sensor_dump_size_bytes):
            sensor_bytes_list.append( serialObj.readByte() )    
            
        
        data_bytes = sensor_bytes_list[ self.low_byte_range : self.upp_byte_range ]
        
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
    
    