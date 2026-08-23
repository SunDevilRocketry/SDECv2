# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .conv_functions import imu_accel, imu_gyro, baro_press
from .sensor import Sensor
from typing import List

def flight_computer_rev2_sensors() -> List[Sensor]:
    """
    Create and return a list of sensors for the Flight Computer Rev 2.0.

    Returns:
        List[Sensor]: List of configured sensors for the Flight Computer Rev 2.0.
    """
    sensor_tuples = [
        (b"\x00", "accXconv", "Pre-converted Accel X", 4, float, "m/s/s", None),
        (b"\x01", "accYconv", "Pre-converted Accel Y", 4, float, "m/s/s", None),
        (b"\x02", "accZconv", "Pre-converted Accel Z", 4, float, "m/s/s", None),
        (b"\x03", "gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s", None),
        (b"\x04", "gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s", None),
        (b"\x05", "gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s", None),
        (b"\x06", "magXconv", "Pre-converted Mag X", 4, float, "µT", None),
        (b"\x07", "magYconv", "Pre-converted Mag Y", 4, float, "µT", None),
        (b"\x08", "magZconv", "Pre-converted Mag Z", 4, float, "µT", None),

        (b"\x09", "quat_w", "Unit Quaternion W", 4, float, "", None),
        (b"\x0A", "quat_x", "Unit Quaternion X", 4, float, "", None),
        (b"\x0B", "quat_y", "Unit Quaternion Y", 4, float, "", None),
        (b"\x0C", "quat_z", "Unit Quaternion Z", 4, float, "", None),
        (b"\x0D", "roll_rate", "Roll Rate", 4, float, "deg/s", None),

        (b"\x0E", "velo", "Velocity", 4, float, "m/s", None),
        (b"\x0F", "velo_x", "Velo X", 4, float, "m/s", None),
        (b"\x10", "velo_y", "Velo Y", 4, float, "m/s", None),
        (b"\x11", "velo_z", "Velo Z", 4, float, "m/s", None),

        (b"\x12", "pres", "Barometric Pressure", 4, float, "Pa", None),
        (b"\x13", "temp", "Barometric Temperature", 4, float, "C", None),
        (b"\x14", "alt", "Barometric Altitude", 4, float, "m", None),

        (b"\x15", "altg", "GPS Altitude (ft)", 4, float, "ft", None),
        (b"\x16", "speedg", "GPS Speed (KmH)", 4, float, "km/h", None),
        (b"\x17", "utc_time", "GPS UTC Time", 4, float, "s", None),
        (b"\x18", "long", "GPS Longitude (deg)", 4, float, "deg", None),
        (b"\x19", "lat", "GPS Latitude (deg)", 4, float, "deg", None),

        (b"\x20", "ns", "GPS North/South", 1, str, "N/S", None),
        (b"\x21", "ew", "GPS East/West", 1, str, "E/W", None),
        (b"\x22", "gll_s", "GPS GLL Status", 1, str, "", None),
        (b"\x23", "rmc_s", "GPS RMC Status", 1, str, "", None),
    ]

    sensors: List[Sensor] = []
    offset = 0

    for poll_code, short_name, name, size, data_type, unit, conv_func in sensor_tuples:
        sensors.append(Sensor(short_name, name, size, data_type, unit, conv_func, poll_code, offset))
        offset += size

    return sensors