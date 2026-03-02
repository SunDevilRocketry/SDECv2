import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Sensor import Sensor
from Sensor import conv_functions
from Sensor.create_sensors import flight_computer_rev2_sensors
from SerialController import SerialSentry, SerialObj, Comport
from typing import List

def test_sensor():
    # Create the firmware object
    appa_firmware = Firmware(
            id=b"\x06",
            name="APPA",
            preset_frame_size=0,
            preset_file=""
        )

    # Use premade functions to create the APPA Rev2 Base Controller
    flight_computer_rev2_controller = create_controllers.flight_computer_rev2_controller()
    appa_fc_rev2_base_controller = BaseController(flight_computer_rev2_controller, appa_firmware)

    # Extract the sensor poll codes from the APPA Rev2 Base Controller
    poll_codes = appa_fc_rev2_base_controller.controller.poll_codes

    # Extract the Sensor objects for the AccX, AccY, and AccZ sensors
    acc_sensors = flight_computer_rev2_sensors()[0:3]

    print(acc_sensors)

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    # Get each acceleration sensor's data dump
    print("Acc readings:")
    for sensor in acc_sensors:
        dump_val = sensor.dump(serial_connection)

        if dump_val:
            print(f"{sensor.name} : {dump_val:.5f} {sensor.unit}")
        else:
            print(f"{sensor.name} : Data Dump returned None")
    
    serial_connection.close_comport()

if __name__ == "__main__":
    test_sensor()