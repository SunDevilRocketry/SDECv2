from BaseController import Firmware
from Sensor import SensorSentry, create_sensors

def test_prints():
    appa_firmware = Firmware(
            id=b"\x06",
            name="APPA",
            preset_frame_size=0,
            preset_file=""
        )

    # Use premade functions to create the APPA Rev2 Sensors
    flight_computer_rev2_sensors = create_sensors.flight_computer_rev2_sensors()

    # Extract the Sensor objects for the Acc{x,y,z} and gyro{x,y,z}conv sensors
    sensor_sentry = SensorSentry(sensors=flight_computer_rev2_sensors)

    print(sensor_sentry.pretty_print())

if __name__ == "__main__":
    test_prints()