from typing import Callable

class Sensor:
    #changes: added offset, size, opcode to init
    def __init__( self, name: str, unit: str, convert_data: Callable[[float], float,], offset : int, size : int, opcode : bytes) :
        self.name = name
        self.unit = unit
        self.convert_data = convert_data
        self.offset = offset
        self.size = size
        self.opcode = opcode
    
    def convert_data( self ) -> float:
        return self.conv_data
        #refactor serial obj 
    def data_dump( self, subcommand, serialObj ) -> float:
        # TODO:
        #check appa.py for list of sensors, substring for dump
        #check hardwarecommand lines 341, 571,
        #commands for opcode
        
        #set command opcode
        #opcode = b'\x03'
        
        #send command opcode
        serialObj.send_byte( self.opcode )
        
        #send sensor dump subcommand code b'\x01' for all sensors
        serialObj.send_byte( subcommand )
        
        
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
    
    