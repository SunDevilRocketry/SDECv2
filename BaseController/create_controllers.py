from .controller import Controller
from .base_sensor import BaseSensor

def flight_computer_rev2_controller() -> Controller:
    # TODO: update when new state estimations for yaw created
    poll_codes = {
        b'\x00': BaseSensor("accX", "Accelerometer X", 2, int, "m/s/s"),
        b'\x01': BaseSensor("accY", "Accelerometer Y", 2, int, "m/s/s"),
        b'\x02': BaseSensor("accZ", "Accelerometer Z", 2, int, "m/s/s"),
        b'\x03': BaseSensor("gyroX", "Gyroscope X", 2, int, "deg/s"),
        b'\x04': BaseSensor("gyroY", "Gyroscope Y", 2, int, "deg/s"),
        b'\x05': BaseSensor("gyroZ", "Gyroscope Z", 2, int, "deg/s"),
        b'\x06': BaseSensor("magX", "Magnetometer X", 2, int, ""),
        b'\x07': BaseSensor("magY", "Magnetometer Y", 2, int, ""),
        b'\x08': BaseSensor("magZ", "Magnetometer Z", 2, int, ""),
        b'\x09': BaseSensor("imut", "IMU Die Temperature", 2, int, "deg C"), # Unused

        b'\x0A': BaseSensor("accXconv", "Pre-converted Accel X", 4, float, "m/s/s"),
        b'\x0B': BaseSensor("accYconv", "Pre-converted Accel Y", 4, float, "m/s/s"),
        b'\x0C': BaseSensor("accZconv", "Pre-converted Accel Z", 4, float, "m/s/s"),
        b'\x0D': BaseSensor("gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s"),
        b'\x0E': BaseSensor("gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s"),
        b'\x0F': BaseSensor("gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s"),

        b'\x10': BaseSensor("rollDeg", "Roll Body Angle", 4, float, "deg"),
        b'\x11': BaseSensor("pitchDeg", "Pitch Body Angle", 4, float, "deg"),
        b'\x12': BaseSensor("rollRate", "Roll Body Rate", 4, float, "deg/s"),
        b'\x13': BaseSensor("pitchRate", "Pitch Body Rate", 4, float, "deg/s"),

        b'\x14': BaseSensor("velo", "Velocity", 4, float, "m/s"),
        b'\x15': BaseSensor("velo_x", "Velo X", 4, float, "m/s"),
        b'\x16': BaseSensor("velo_y", "Velo Y", 4, float, "m/s"),
        b'\x17': BaseSensor("velo_z", "Velo Z", 4, float, "m/s"),

        b'\x18': BaseSensor("pos", "Position", 4, float, "m"),
        b'\x19': BaseSensor("pres", "Barometric Pressure", 4, float, "kPa"),
        b'\x1A': BaseSensor("temp", "Barometric Temperature", 4, float, "C"),
        b'\x1B': BaseSensor("alt", "Barometric Altitude", 4, float, "m"),
        b'\x1C': BaseSensor("bvelo", "Barometric Velocity", 4, float, "m/s"),

        b'\x1D': BaseSensor("altg", "GPS Altitude (ft)", 4, float, "ft"),
        b'\x1E': BaseSensor("speedg", "GPS Speed (KmH)", 4, float, "km/h"),
        b'\x1F': BaseSensor("utc_time", "GPS UTC Time", 4, float, "s"),
        b'\x20': BaseSensor("long", "GPS Longitude (deg)", 4, float, "deg"),
        b'\x21': BaseSensor("lat", "GPS Latitude (deg)", 4, float, "deg"),

        b'\x22': BaseSensor("ns", "GPS North/South", 1, str, "N/S"),
        b'\x23': BaseSensor("ew", "GPS East/West", 1, str, "E/W"),
        b'\x24': BaseSensor("gll_s", "GPS GLL Status", 1, str, ""),
        b'\x25': BaseSensor("rmc_s", "GPS RMC Status", 1, str, "")
    }

    return Controller(
        id=b"\x05",
        name="Flight Computer (A0002 Rev 2.0)",
        poll_codes=poll_codes,
        sensor_frame_size=126,
        sensor_data_file="output/flight_comp_rev2_sensor_data.txt"
    )
