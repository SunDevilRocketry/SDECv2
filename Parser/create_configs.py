from .bitmask import FeatureBitmask, DataBitmask
from .data import Data
from .feature import Feature
from .toggle import Toggle
from BaseController import BaseSensor

def appa_feature_bitmask() -> FeatureBitmask:
    features = [
        Feature(
            name="Data Logging",
            value=Toggle.ENABLED
        ),
        Feature(
            name="Dual Deploy",
            value=Toggle.DISABLED
        ),
        Feature(
            name="Active Roll Control",
            value=Toggle.DISABLED
        ),
        Feature(
            name="Active Pitch Yaw Control",
            value=Toggle.DISABLED
        ),
        Feature(
            name="Wireless Transmission",
            value=Toggle.DISABLED
        ),
        Feature(
            name="Launch Detect Baro",
            value=Toggle.ENABLED
        ),
        Feature(
            name="Launch Detect Accel",
            value=Toggle.ENABLED
        ),
        Feature(
            name="GPS",
            value=Toggle.DISABLED
        )
    ]

    return FeatureBitmask(features=features)

def appa_data_bitmask() -> DataBitmask:
    datas = [
        Data(
            name="conv",
            value=Toggle.ENABLED,
            sensors=[
                BaseSensor("accXconv", "Pre-converted Accel X", 4, float, "m/s/s"),
                BaseSensor("accYconv", "Pre-converted Accel Y", 4, float, "m/s/s"),
                BaseSensor("accZconv", "Pre-converted Accel Z", 4, float, "m/s/s"),
                
                BaseSensor("gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s"),
                BaseSensor("gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s"),
                BaseSensor("gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s"),

                BaseSensor("magXconv", "Pre-converted Magnetometer X", 4, float, "deg/s"),
                BaseSensor("magYconv", "Pre-converted Magnetometer Y", 4, float, "deg/s"),
                BaseSensor("magZconv", "Pre-converted Magnetometer Z", 4, float, "deg/s"),

                BaseSensor("pressure", "Barometric Pressure", 4, float, "kPa"),
                BaseSensor("temp", "Barometric Temperature", 4, float, "C")
            ]
        ),
        Data(
            name="state_estim",
            value=Toggle.ENABLED,
            sensors=[
                BaseSensor("rollDeg", "Roll Body Angle", 4, float, "deg"),
                BaseSensor("pitchDeg", "Pitch Body Angle", 4, float, "deg"),
                BaseSensor("yawDeg", "Yaw Body Angle", 4, float, "deg"),
                BaseSensor("rollRate", "Roll Body Rate", 4, float, "deg/s"),
                BaseSensor("pitchRate", "Pitch Body Rate", 4, float, "deg/s"),
                BaseSensor("yawRate", "Yaw Body Rate", 4, float, "deg/s"),
                
                BaseSensor("velo", "Velocity", 4, float, "m/s"),
                BaseSensor("velo_x", "Velo X", 4, float, "m/s"),
                BaseSensor("velo_y", "Velo Y", 4, float, "m/s"),
                BaseSensor("velo_z", "Velo Z", 4, float, "m/s"),
                
                BaseSensor("pos", "Position", 4, float, "m"),

                BaseSensor("alt", "Barometric Altitude", 4, float, "m"),
                BaseSensor("bvelo", "Barometric Velocity", 4, float, "m/s")
            ]
        ),
        Data(
            name="gps",
            value=Toggle.ENABLED,
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
        Data(
            name="canard",
            value=Toggle.DISABLED,
            sensors=[
                BaseSensor("feedback", "Canard Feedback", 4, float, "")
            ]
        )
    ]

    return DataBitmask(datas=datas)
