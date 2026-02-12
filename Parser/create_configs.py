from .bitmask import FeatureBitmask, DataBitmask
from .data import Data
from .feature import Feature
from .preset_config import PresetConfig, PresetEntry, ConfigData, ImuPreset, BaroPreset, ServoPreset, PresetChecksum, PresetDataBitmask, PresetFeatureBitmask
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
        Data(
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
        Data(
            name="state_estim",
            value=Toggle.ENABLED,
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

def appa_preset_config() -> PresetConfig:
    return PresetConfig(
        config_data=ConfigData(
            checksum=PresetChecksum(),
            feature_bitmask=PresetFeatureBitmask(),
            data_bitmask=PresetDataBitmask(),
            entries=[
                PresetEntry("Sensor calib samples", 2, int),
                PresetEntry("LD timeout", 2, int),
                PresetEntry("LD baro threshold", 2, int),
                PresetEntry("LD accel threshold", 1, int),
                PresetEntry("LD accel samples", 1, int),
                PresetEntry("LD baro samples", 1, int),
                PresetEntry("Pad byte", 1, int),
                PresetEntry("Flash rate limit", 2, int),
                PresetEntry("Apogee detect samples", 1, int),
                PresetEntry("AC max deflect angle", 1, int),
                PresetEntry("AR Delay after launch", 2, int),
                PresetEntry("AC Roll PID P const", 4, float),
                PresetEntry("AC Roll PID I const", 4, float),
                PresetEntry("AC Roll PID D const", 4, float),
                PresetEntry("AC P/Y PID P const", 4, float),
                PresetEntry("AC P/Y PID I const", 4, float),
                PresetEntry("AC P/Y PID D const", 4, float)
            ]
        ),
        imu_preset=ImuPreset([
            PresetEntry("Accel x offset", 4, float),
            PresetEntry("Accel y offset", 4, float),
            PresetEntry("Accel z offset", 4, float),
            PresetEntry("Gyro x offset", 4, float),
            PresetEntry("Gyro y offset", 4, float),
            PresetEntry("Gyro z offset", 4, float)
        ]),
        baro_preset=BaroPreset([
            PresetEntry("Baro pres offset", 4, float),
            PresetEntry("Baro temp offset", 4, float)
        ]),
        servo_preset=ServoPreset([
            PresetEntry("Servo 1 RP", 1, int),
            PresetEntry("Servo 2 RP", 1, int),
            PresetEntry("Servo 3 RP", 1, int),
            PresetEntry("Servo 4 RP", 1, int)
        ])
    )