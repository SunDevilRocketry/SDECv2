from .bitmask import FeatureBitmask, DataBitmask
from .data import Data
from .feature import Feature
from .preset_config import PresetConfig, ConfigEntry
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

def appa_feature_bitmask_from_bits(bits: str) -> FeatureBitmask:
    appa_features = appa_feature_bitmask().features
    if len(bits) != 8:
        raise ValueError(f"Bitmask {bits} is not length 8")
    
    features = []
    for bit, feature in zip(reversed(bits), appa_features):
        features.append(
            Feature(
                name=feature.name, 
                value=Toggle.ENABLED if bit == "1" else Toggle.DISABLED
            )
        )

    return FeatureBitmask(features=features)

def appa_data_bitmask_from_bits(bits: str) -> DataBitmask:
    appa_datas = appa_data_bitmask().datas
    if len(bits) != 8:
        raise ValueError(f"Bitmask {bits} is not length 8")
    
    datas = []
    for bit, data in zip(reversed(bits), appa_datas):
        datas.append(
            Data(
                name=data.name, 
                value=Toggle.ENABLED if bit == "1" else Toggle.DISABLED,
                sensors=data.sensors
            )
        )

    return DataBitmask(datas=datas)

def appa_preset_config() -> PresetConfig:
    return PresetConfig(
        data_config=[
            ConfigEntry("Sensor calib samples", 2, int),
            ConfigEntry("LD timeout", 2, int),
            ConfigEntry("LD baro threshold", 2, int),
            ConfigEntry("LD accel threshold", 1, int),
            ConfigEntry("LD accel samples", 1, int),
            ConfigEntry("LD baro samples", 1, int),
            ConfigEntry("Pad byte", 1, int),
            ConfigEntry("Flash rate limit", 2, int),
            ConfigEntry("Apogee detect samples", 1, int),
            ConfigEntry("AC max deflect angle", 1, int),
            ConfigEntry("AR Delay after launch", 2, int),
            ConfigEntry("AC Roll PID P const", 4, float),
            ConfigEntry("AC Roll PID I const", 4, float),
            ConfigEntry("AC Roll PID D const", 4, float),
            ConfigEntry("AC P/Y PID P const", 4, float),
            ConfigEntry("AC P/Y PID I const", 4, float),
            ConfigEntry("AC P/Y PID D const", 4, float)
        ],
        imu_config=[
            ConfigEntry("Accel x offset", 4, float),
            ConfigEntry("Accel y offset", 4, float),
            ConfigEntry("Accel z offset", 4, float),
            ConfigEntry("Gyro x offset", 4, float),
            ConfigEntry("Gyro y offset", 4, float),
            ConfigEntry("Gyro z offset", 4, float)
        ],
        baro_config=[
            ConfigEntry("Baro pres offset", 4, float),
            ConfigEntry("Baro temp offset", 4, float)
        ],
        servo_config=[
            ConfigEntry("Servo 1 RP", 1, int),
            ConfigEntry("Servo 2 RP", 1, int),
            ConfigEntry("Servo 3 RP", 1, int),
            ConfigEntry("Servo 4 RP", 1, int)
        ]
    )