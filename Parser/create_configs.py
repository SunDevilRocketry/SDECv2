from .bitmask import Bitmask
from .feature import Feature
from .toggle import Toggle
from BaseController import BaseSensor

def appa_bitmask() -> Bitmask:
    features = [
        Feature(
            name="raw",
            value=Toggle.ENABLED,
            sensors=[
                BaseSensor("accX", "Accelerometer X", 2, int, "m/s/s"),
                BaseSensor("accY", "Accelerometer Y", 2, int, "m/s/s"),
                BaseSensor("accZ", "Accelerometer Z", 2, int, "m/s/s"),
                
                BaseSensor("gyroX", "Gyroscope X", 2, int, "deg/s"),
                BaseSensor("gyroY", "Gyroscope Y", 2, int, "deg/s"),
                BaseSensor("gyroZ", "Gyroscope Z", 2, int, "deg/s"),
                
                BaseSensor("magX", "Magnetometer X", 2, int, ""),
                BaseSensor("magY", "Magnetometer Y", 2, int, ""),
                BaseSensor("magZ", "Magnetometer Z", 2, int, ""),
                
                BaseSensor("imut", "IMU Die Temperature", 2, int, "deg C"),
                BaseSensor("pres", "Barometric Pressure", 4, float, "kPa"),
                BaseSensor("temp", "Barometric Temperature", 4, float, "C")
            ]
        ),
        Feature(
            name="conv",
            value=Toggle.ENABLED,
            sensors=[
                BaseSensor("accXconv", "Pre-converted Accel X", 4, float, "m/s/s"),
                BaseSensor("accYconv", "Pre-converted Accel Y", 4, float, "m/s/s"),
                BaseSensor("accZconv", "Pre-converted Accel Z", 4, float, "m/s/s"),
                
                BaseSensor("gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s"),
                BaseSensor("gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s"),
                BaseSensor("gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s")
            ]
        ),
        Feature(
            name="state_estim",
            value=Toggle.DISABLED,
            sensors=[
                BaseSensor("rollDeg", "Roll Body Angle", 4, float, "deg"),
                BaseSensor("pitchDeg", "Pitch Body Angle", 4, float, "deg"),
                BaseSensor("rollRate", "Roll Body Rate", 4, float, "deg/s"),
                BaseSensor("pitchRate", "Pitch Body Rate", 4, float, "deg/s"),
                
                BaseSensor("velo", "Velocity", 4, float, "m/s"),
                BaseSensor("velo_x", "Velo X", 4, float, "m/s"),
                BaseSensor("velo_y", "Velo Y", 4, float, "m/s"),
                BaseSensor("velo_z", "Velo Z", 4, float, "m/s"),
                
                BaseSensor("pos", "Position", 4, float, "m"),
                BaseSensor("alt", "Barometric Altitude", 4, float, "m"),
                BaseSensor("bvelo", "Barometric Velocity", 4, float, "m/s")
            ]
        ),
        Feature(
            name="gps",
            value=Toggle.DISABLED,
            sensors=[
                BaseSensor("altg", "GPS Altitude (ft)", 4, float, "ft"),
                BaseSensor("speedg", "GPS Speed (KmH)", 4, float, "km/h"),
                BaseSensor("utc_time", "GPS UTC Time", 4, float, "s"),
                BaseSensor("long", "GPS Longitude (deg)", 4, float, "deg"),
                BaseSensor("lat", "GPS Latitude (deg)", 4, float, "deg"),

                BaseSensor("ns", "GPS North/South", 1, str, "N/S"),
                BaseSensor("ew", "GPS East/West", 1, str, "E/W"),
                BaseSensor("gll_s", "GPS GLL Status", 1, str, ""),
                BaseSensor("rmc_s", "GPS RMC Status", 1, str, "")
            ]
        ),
        Feature(
            name="canard",
            value=Toggle.ENABLED,
            sensors=[
                BaseSensor("feedback", "Canard Feedback", 4, float, "")
            ]
        )
    ]

    return Bitmask(features=features)
