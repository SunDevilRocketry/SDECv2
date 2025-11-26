import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Sensor import Sensor, SensorSentry
from Sensor import conv_functions, create_sensors
from SerialController import SerialSentry, SerialObj, Comport

def test_sensor():
    # Create the firmware object
    appa_firmware = Firmware(
            id=b"\x06",
            name="APPA",
            preset_frame_size=0,
            preset_file=""
        )

    # Use premade functions to create the APPA Rev2 Sensors
    flight_computer_rev2_sensors = create_sensors.flight_computer_rev2_sensors()

    # Extract the Sensor objects for the Acc{x,y,z} and gyro{x,y,z}conv sensors
    sensor_sentry = SensorSentry()

    for sensor in flight_computer_rev2_sensors:
        if sensor.poll_code in {b"\x00", b"\x01", b"\x02", b"\x0D", b"\x0E", b"\x0F"}:
            sensor_sentry.add_sensor(sensor)

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM3", 921600, 5)
    serial_connection.open_comport()

    # Get the sensor poll from the sentry
    print("Sentry Poll (2 seconds):")
    for sensor_poll in sensor_sentry.poll(serial_connection, timeout=2):
        for sensor, readout in sensor_poll.items():
            if readout:
                print(f"{sensor.name}: {readout:.2f} {sensor.unit}")
            else:
                print(f"{sensor.name}: 0.0 {sensor.unit}")

    print("Sentry Poll (count 10):")
    for sensor_poll in sensor_sentry.poll(serial_connection, count=10):
        for sensor, readout in sensor_poll.items():
            if readout:
                print(f"{sensor.name}: {readout:.2f} {sensor.unit}")
            else:
                print(f"{sensor.name}: 0.0 {sensor.unit}")

    serial_connection.close_comport()

if __name__ == "__main__":
    test_sensor()