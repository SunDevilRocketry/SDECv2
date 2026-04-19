# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .controller import Controller
from .base_sensor import BaseSensor
from SDECv2.Sensor import create_sensors

def create_controller(hardware_id) -> Controller:
    """
    Create and return a controller matching a given hardware code.

    Returns:
        Controller: for the given ID.
    """
    if( hardware_id == b'\x05' ):
        return flight_computer_rev2_controller()
    elif( hardware_id == b'\x10' ):
        return ground_station_rev1_controller()

def flight_computer_rev2_controller() -> Controller:
    """
    Create and return a controller for the Flight Computer Rev 2.0.

    Returns:
        Controller: Configured controller instance for the Flight Computer Rev 2.0.
    """
    poll_codes = {
        sensor.poll_code: BaseSensor(
            sensor.short_name, 
            sensor.name, 
            sensor.size, 
            sensor.data_type, 
            sensor.unit
        ) for sensor in create_sensors.flight_computer_rev2_sensors()
    }

    return Controller(
        id=b"\x05",
        name="Flight Computer (A0002 Rev 2.0)",
        poll_codes=poll_codes,
        sensor_frame_size=120,
        sensor_data_file="output/flight_comp_rev2_sensor_data.txt"
    )

def ground_station_rev1_controller() -> Controller:
    """
    Create and return a controller for the Ground Station Rev 1.0.

    Returns:
        Controller: Configured controller instance for the Ground Station Rev 1.0.
    """
    return Controller(
        id=b"\x10",
        name="Ground Station (Rev 1.0)",
        poll_codes={},
        sensor_frame_size=0,
        sensor_data_file=""
    )

