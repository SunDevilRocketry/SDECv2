# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .firmware import Firmware

def appa_firmware() -> Firmware:
    """
    Create and return a Firmware for the v2.5.0 APPA Flight Comptuer Firmware

    Returns:
        Firmmware: Configured firmware instance for the v2.5.0 APPA Flight Computer Firmware
    """
    return Firmware(
        id=b"\x06",
        name="APPA",
        preset_frame_size=0,
        preset_file="",
    )

def flight_transmitter_firmware() -> Firmware:
    """
    Create and return a Firmware for the Ground Station Flight Transmitter Firmware.

    Returns:
        Firemware: Configured firmware instance for the Ground Station Flight Transmitter Firmware.
    """
    return Firmware(
        id=b"\x07",
        name="Flight Transmitter Firmware",
        preset_frame_size=0,
        preset_file="",
    )