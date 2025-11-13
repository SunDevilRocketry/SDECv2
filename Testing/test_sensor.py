from BaseController import *
from BaseController import create_controllers
from Sensor import Sensor
from SerialController import SerialSentry, SerialObj, Comport

def conv_fucntion(raw_data: float) -> float:
    return raw_data * 2.0 # Example conversion logic

serial_connection = SerialObj()

sensor = Sensor(
    name = "Test Sensor",
    unit = "units",
    convert_data = conv_fucntion,
    offset = 4, 
    size = 2,
    opcode = b'\x03',
    data_type=int
)

print(f"Sensor Name: {sensor.name}")
print(f"Sensor Unit: {sensor.unit}")
#convert data example call
print(f"Converted Data: {sensor.convert_data(10.0)}")  # Example raw data input

print(f"Data Dump: {sensor.data_dump(b'\x01', serial_connection)}")  # Example subcommand

# Make base controller
appa_firmware = Firmware(
        id=b"\x06",
        name="APPA",
        preset_frame_size=0,
        preset_file=""
    )

flight_computer_rev2_callable = create_controllers.flight_computer_rev2_controller

appa_fc_rev2_base_controller = BaseController(flight_computer_rev2_callable, appa_firmware)

poll_codes = appa_fc_rev2_base_controller.controller.poll_codes

#prototype making full list of sensor using dictionary from base controller just first three though and do those tests i have above
#do for loop down here

#this for loop to test all sensors
#for sensor in poll_codes.values(): 

for poll_code, base_sensor in poll_codes.items():
    new_sensor = Sensor(
        name=base_sensor.name,
        unit=base_sensor.unit,
        convert_data=conv_fucntion,
        offset=2,
        size=2,
        opcode=poll_code,
        data_type=base_sensor.data_type
    )

    #new_sensor.data_dump()



"""
    appa_sensor_sizes = {
    "raw": {
        "accX" :         2,
        "accY" :         2,
        "accZ" :         2,
        "gyroX":         2,
        "gyroY":         2,
        "gyroZ":         2,
        "magX" :         2,
        "magY" :         2,
        "magZ" :         2,
        "imut" :         2,
        "pres" :         4,
        "temp" :         4
        """