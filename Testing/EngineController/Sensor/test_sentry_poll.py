import time

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Sensor import Sensor, SensorSentry
from Sensor import conv_functions, create_sensors
from SerialController import SerialSentry, SerialObj, Comport

def test_sensor():
    # Use premade functions to create the Engine Sensors
    engine_controller_rev5_sensors = create_sensors.engine_controller_rev5_sensors()

    # Extract the Sensor objects for the PT0, PT1, PT2
    sensor_sentry = SensorSentry()

    for sensor in engine_controller_rev5_sensors:
        if sensor.poll_code in {b"\x00", b"\x01", b"\x02"}:
            sensor_sentry.add_sensor(sensor)

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
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