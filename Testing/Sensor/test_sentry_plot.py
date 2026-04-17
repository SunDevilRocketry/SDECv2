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

    # Extract the Sensor objects for the Acc{x,y,z} sensors
    sensor_sentry = SensorSentry()

    for sensor in flight_computer_rev2_sensors:
        if sensor.poll_code in {b"\x00", b"\x01", b"\x02", b"\x03", b"\x04", b"\x05"}:
            sensor_sentry.add_sensor(sensor)

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    # Plot all sensors for 5 seconds
    print("Sentry Plot (5 seconds):")
    sensor_sentry.plot(serial_connection, timeout=5)

    # Plot a subset of sensors for 10 counts
    sensors_to_plot = [s for s in sensor_sentry.sensors if s.poll_code in {b"\x00", b"\x01", b"\x02"}]
    print("Sentry Plot (count 10, AccX/Y/Z only):")
    sensor_sentry.plot(serial_connection, count=10, sensors=sensors_to_plot)

    serial_connection.close_comport()

if __name__ == "__main__":
    test_sensor()
