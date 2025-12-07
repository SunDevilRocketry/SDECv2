import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Sensor import Sensor
from Sensor import conv_functions
from SerialController import SerialSentry, SerialObj, Comport

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

    # Extract the Sensor objects for the AccX
    acc_sensors = []
    offset = 0

    poll_code, base_sensor = next(iter(poll_codes.items()))
    acc_x = Sensor(
            short_name=base_sensor.short_name,
            name=base_sensor.name,
            size=base_sensor.size,
            data_type=base_sensor.data_type,
            unit=base_sensor.unit,
            convert_data=conv_functions.imu_accel,
            poll_code=poll_code,
            offset=offset
        )

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM3", 921600, 5)
    serial_connection.open_comport()

    # Poll AccX for 2 seconds
    print("AccX readings (2 second poll):")
    for reading in acc_x.poll(serial_connection, timeout=2): print(f"{reading:.2f} {acc_x.unit}")

    # Poll AccX for 10 readings
    print("AccX readings: (10 count poll)")
    for reading in acc_x.poll(serial_connection, count=10): print(f"{reading:.2f} {acc_x.unit}")

     # Poll AccX for nothing
    print("AccX readings: (nothing)")
    for reading in acc_x.poll(serial_connection): print(f"{reading:.2f} {acc_x.unit}")
    
    serial_connection.close_comport()

if __name__ == "__main__":
    test_sensor()