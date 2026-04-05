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

def receiver_firmware() -> Firmware:
    """
    Create and return a Firmware for the Receiver Firmware.

    Returns:
        Firemware: Configured firmware instance for the Receiver Firmware.
    """
    return Firmware(
        id=b"\x11",
        name="Receiver Firmware",
        preset_frame_size=0,
        preset_file="",
    )