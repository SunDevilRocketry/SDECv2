from Sensor import SensorSentry
from Sensor import create_sensors
from SerialController import SerialObj

def test_sensor():
    # Use premade functions to create the Engine Sensors
    engine_controller_rev5_sensors = create_sensors.engine_controller_rev5_sensors()

    # Extract the Sensor objects for the Acc{x,y,z} and gyro{x,y,z}conv sensors
    sensor_sentry = SensorSentry(sensors=engine_controller_rev5_sensors)

    # Create the serial connection
    serial_connection = SerialObj()
    serial_connection.init_comport("COM6", 921600, 5)
    serial_connection.open_comport()

    # Get the sensor dump from the sentry
    print("Sentry Dump:")
    sensor_dump = sensor_sentry.dump(serial_connection)

    for sensor, readout in sensor_dump.items():
        if readout:
            print(f"{sensor.name}: {readout:.2f} {sensor.unit}")
        else:
            print(f"{sensor.name}: 0.0 {sensor.unit}")

    serial_connection.close_comport()

if __name__ == "__main__":
    test_sensor()