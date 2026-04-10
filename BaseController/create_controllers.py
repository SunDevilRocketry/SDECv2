# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .controller import Controller
from .base_sensor import BaseSensor
from SDECv2.Sensor import create_sensors

def flight_computer_rev2_controller() -> Controller:
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

def engine_controller_rev5_controller() -> Controller:
    poll_codes = {
        sensor.poll_code: BaseSensor(
            sensor.short_name,
            sensor.name,
            sensor.size,
            sensor.data_type,
            sensor.unit
        ) for sensor in create_sensors.engine_controller_rev5_sensors()
    }

    return Controller(
        id=b"\x08",
        name="Liquid Engine Controller (L0002 Rev 5.0)",
        poll_codes=poll_codes,
        sensor_frame_size=44,
        sensor_data_file="output/engine_ctrl_rev5_sensor_data.txt"
    )
