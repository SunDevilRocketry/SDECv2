# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .conv_functions import imu_accel, imu_gyro, baro_press, pt_pressure, pt_pressure_5V, tc_temp, loadcell_force
from .sensor import Sensor
from typing import List

def flight_computer_rev2_sensors() -> List[Sensor]:
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

        (b"\x09", "rollDeg", "Roll Body Angle", 4, float, "deg", None),
        (b"\x0A", "pitchDeg", "Pitch Body Angle", 4, float, "deg", None),
        (b"\x0B", "yawDeg", "Yaw Body Angle", 4, float, "deg", None),
        (b"\x0C", "rollRate", "Roll Body Rate", 4, float, "deg/s", None),
        (b"\x0D", "pitchRate", "Pitch Body Rate", 4, float, "deg/s", None),
        (b"\x0E", "yawRate", "Yaw Body Rate", 4, float, "deg/s", None),

        (b"\x0F", "velo", "Velocity", 4, float, "m/s", None),
        (b"\x10", "velo_x", "Velo X", 4, float, "m/s", None),
        (b"\x11", "velo_y", "Velo Y", 4, float, "m/s", None),
        (b"\x12", "velo_z", "Velo Z", 4, float, "m/s", None),

        (b"\x13", "pos", "Position", 4, float, "m", None),
        (b"\x14", "pres", "Barometric Pressure", 4, float, "kPa", baro_press),
        (b"\x15", "temp", "Barometric Temperature", 4, float, "C", None),
        (b"\x16", "alt", "Barometric Altitude", 4, float, "m", None),
        (b"\x17", "bvelo", "Barometric Velocity", 4, float, "m/s", None),

        (b"\x18", "altg", "GPS Altitude (ft)", 4, float, "ft", None),
        (b"\x19", "speedg", "GPS Speed (KmH)", 4, float, "km/h", None),
        (b"\x1A", "utc_time", "GPS UTC Time", 4, float, "s", None),
        (b"\x1B", "long", "GPS Longitude (deg)", 4, float, "deg", None),
        (b"\x1C", "lat", "GPS Latitude (deg)", 4, float, "deg", None),

        (b"\x1D", "ns", "GPS North/South", 1, str, "N/S", None),
        (b"\x1E", "ew", "GPS East/West", 1, str, "E/W", None),
        (b"\x1F", "gll_s", "GPS GLL Status", 1, str, "", None),
        (b"\x20", "rmc_s", "GPS RMC Status", 1, str, "", None),
    ]

    sensors: List[Sensor] = []
    offset = 0

    for poll_code, short_name, name, size, data_type, unit, conv_func in sensor_tuples:
        sensors.append(Sensor(short_name, name, size, data_type, unit, conv_func, poll_code, offset))
        offset += size

    return sensors

def rev2_dashboard_dump_sensors() -> List[Sensor]:
    sensor_tuples = [
        (b"\x00", "accXconv", "Pre-converted Accel X", 4, float, "m/s/s", None),
        (b"\x01", "accYconv", "Pre-converted Accel Y", 4, float, "m/s/s", None),
        (b"\x02", "accZconv", "Pre-converted Accel Z", 4, float, "m/s/s", None),
        (b"\x03", "gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s", None),
        (b"\x04", "gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s", None),
        (b"\x05", "gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s", None),

        (b"\x09", "rollDeg", "Roll Body Angle", 4, float, "deg", None),
        (b"\x0A", "pitchDeg", "Pitch Body Angle", 4, float, "deg", None),
        (b"\x0B", "yawDeg", "Yaw Body Angle", 4, float, "deg", None),
        (b"\x0C", "rollRate", "Roll Body Rate", 4, float, "deg/s", None),
        (b"\x0D", "pitchRate", "Pitch Body Rate", 4, float, "deg/s", None),
        (b"\x0E", "yawRate", "Yaw Body Rate", 4, float, "deg/s", None),

        (b"\x14", "pres", "Barometric Pressure", 4, float, "kPa", baro_press),
        (b"\x15", "temp", "Barometric Temperature", 4, float, "C", None),
        (b"\x16", "alt", "Barometric Altitude", 4, float, "m", None),
        (b"\x17", "bvelo", "Barometric Velocity", 4, float, "m/s", None),

        (b"\x1B", "long", "GPS Longitude (deg)", 4, float, "deg", None),
        (b"\x1C", "lat", "GPS Latitude (deg)", 4, float, "deg", None),
    ]

    sensors: List[Sensor] = []
    offset = 0

    for poll_code, short_name, name, size, data_type, unit, conv_func in sensor_tuples:
        sensors.append(Sensor(short_name, name, size, data_type, unit, conv_func, poll_code, offset))
        offset += size

    return sensors

def engine_controller_rev5_sensors() -> List[Sensor]:
    """Create the sensor list for the Liquid Engine Controller (L0002 Rev 5.0).

    Returns 10 sensors in poll-code order (``0x00``–``0x09``)::

        pt0  LOX Pressure          psi
        pt1  LOX Flow Upstream     psi
        pt2  LOX Flow Downstream   psi
        pt3  PT3                   psi
        pt4  Engine Pressure       psi
        pt5  Fuel Flow Downstream  psi
        pt6  Fuel Flow Upstream    psi
        pt7  Fuel Pressure         psi
        tc   Thermocouple          °C
        lc   Load Cell             lb

    All sensors carry raw ``int`` values (4 bytes each) with their
    respective conversion functions pre-attached.

    :returns: Ordered list of :class:`~SDECv2.Sensor.sensor.Sensor` objects.
    :rtype: List[Sensor]
    """
    sensor_tuples = [
        (b"\x00", "pt0", "LOX Pressure",        4, int, "psi", pt_pressure),
        (b"\x01", "pt1", "LOX Flow Upstream",    4, int, "psi", pt_pressure),
        (b"\x02", "pt2", "LOX Flow Downstream",  4, int, "psi", pt_pressure),
        (b"\x03", "pt3", "PT3",                  4, int, "psi", pt_pressure),
        (b"\x04", "pt4", "Engine Pressure",      4, int, "psi", pt_pressure),
        (b"\x05", "pt5", "Fuel Flow Downstream", 4, int, "psi", pt_pressure),
        (b"\x06", "pt6", "Fuel Flow Upstream",   4, int, "psi", pt_pressure),
        (b"\x07", "pt7", "Fuel Pressure",        4, int, "psi", pt_pressure),
        (b"\x08", "tc",  "Thermocouple",         4, int, "C",   tc_temp),
        (b"\x09", "lc",  "Load Cell",            4, int, "lb",  loadcell_force),
    ]

    sensors: List[Sensor] = []
    offset = 0

    for poll_code, short_name, name, size, data_type, unit, conv_func in sensor_tuples:
        sensors.append(Sensor(short_name, name, size, data_type, unit, conv_func, poll_code, offset))
        offset += size

    return sensors