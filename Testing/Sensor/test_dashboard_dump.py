import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Sensor import SensorSentry
from SerialController import SerialSentry, SerialObj, Comport
from typing import List

def test_dashboard_dump():
    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    sensor_dump = SensorSentry.dashboard_dump(serial_connection)
    
    for sensor, readout in sensor_dump.items():
        if readout:
            print(f"{sensor.name}: {readout:.2f} {sensor.unit}")
        else:
            print(f"{sensor.name}: 0.0 {sensor.unit}")

    serial_connection.close_comport()

if __name__ == "__main__":
    test_dashboard_dump()