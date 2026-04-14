import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Parser import Telemetry
from SerialController import SerialSentry, SerialObj, Comport
from typing import List

def test_dashboard_dump():
    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    serial_connection.connect()

    telem_obj = Telemetry()

    if( serial_connection.target.controller.id == b'\x05' ):
        # FC version
        telem_obj.dashboard_dump()
        print(telem_obj.get_latest_dashboard_dump())
    else:
        # Other platforms
        print("Testing script not yet implemented for ground station. Sorry!")

    serial_connection.close_comport()

if __name__ == "__main__":
    test_dashboard_dump()