# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .conv_functions import imu_accel, imu_gyro, baro_press
from .sensor import Sensor
from typing import List

def flight_computer_rev2_sensors() -> List[Sensor]:
    sensor_tuples = [
        (b'\x00', "accX", "Accelerometer X", 2, int, "m/s/s", imu_accel),
        (b'\x01', "accY", "Accelerometer Y", 2, int, "m/s/s", imu_accel),
        (b'\x02', "accZ", "Accelerometer Z", 2, int, "m/s/s", imu_accel),
        (b'\x03', "gyroX", "Gyroscope X", 2, int, "deg/s", imu_gyro),
        (b'\x04', "gyroY", "Gyroscope Y", 2, int, "deg/s", imu_gyro),
        (b'\x05', "gyroZ", "Gyroscope Z", 2, int, "deg/s", imu_gyro),
        (b'\x06', "magX", "Magnetometer X", 2, int, "", None),
        (b'\x07', "magY", "Magnetometer Y", 2, int, "", None),
        (b'\x08', "magZ", "Magnetometer Z", 2, int, "", None),
        (b'\x09', "imut", "IMU Die Temperature", 2, int, "deg C", None),

        (b'\x0A', "accXconv", "Pre-converted Accel X", 4, float, "m/s/s", None),
        (b'\x0B', "accYconv", "Pre-converted Accel Y", 4, float, "m/s/s", None),
        (b'\x0C', "accZconv", "Pre-converted Accel Z", 4, float, "m/s/s", None),
        (b'\x0D', "gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s", None),
        (b'\x0E', "gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s", None),
        (b'\x0F', "gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s", None),

        (b'\x10', "rollDeg", "Roll Body Angle", 4, float, "deg", None),
        (b'\x11', "pitchDeg", "Pitch Body Angle", 4, float, "deg", None),
        (b'\x12', "yawDeg", "Yaw Body Angle", 4, float, "deg", None),
        (b'\x13', "rollRate", "Roll Body Rate", 4, float, "deg/s", None),
        (b'\x14', "pitchRate", "Pitch Body Rate", 4, float, "deg/s", None),
        (b'\x15', "yawRate", "Yaw Body Rate", 4, float, "deg/s", None),

        (b'\x16', "velo", "Velocity", 4, float, "m/s", None),
        (b'\x17', "velo_x", "Velo X", 4, float, "m/s", None),
        (b'\x18', "velo_y", "Velo Y", 4, float, "m/s", None),
        (b'\x19', "velo_z", "Velo Z", 4, float, "m/s", None),

        (b'\x1A', "pos", "Position", 4, float, "m", None),
        (b'\x1B', "pres", "Barometric Pressure", 4, float, "kPa", baro_press),
        (b'\x1C', "temp", "Barometric Temperature", 4, float, "C", None),
        (b'\x1D', "alt", "Barometric Altitude", 4, float, "m", None),
        (b'\x1E', "bvelo", "Barometric Velocity", 4, float, "m/s", None),

        (b'\x1F', "altg", "GPS Altitude (ft)", 4, float, "ft", None),
        (b'\x20', "speedg", "GPS Speed (KmH)", 4, float, "km/h", None),
        (b'\x21', "utc_time", "GPS UTC Time", 4, float, "s", None),
        (b'\x22', "long", "GPS Longitude (deg)", 4, float, "deg", None),
        (b'\x23', "lat", "GPS Latitude (deg)", 4, float, "deg", None),

        (b'\x24', "ns", "GPS North/South", 1, str, "N/S", None),
        (b'\x25', "ew", "GPS East/West", 1, str, "E/W", None),
        (b'\x26', "gll_s", "GPS GLL Status", 1, str, "", None),
        (b'\x27', "rmc_s", "GPS RMC Status", 1, str, "", None),
    ]

    sensors: List[Sensor] = []
    offset = 0

    for poll_code, short_name, name, size, data_type, unit, conv_func in sensor_tuples:
        sensors.append(Sensor(short_name, name, size, data_type, unit, conv_func, poll_code, offset))
        offset += size

    return sensors