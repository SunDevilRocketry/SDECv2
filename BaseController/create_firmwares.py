# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .firmware import Firmware

def create_firmware(firmware_id) -> Firmware:
    """
    Create and return a firmware object matching a given firmware code.

    Returns:
        Firmware for the given ID.
    """
    if( firmware_id == b'\x06' ):
        return appa_firmware()
    elif( firmware_id == b'\x11' ):
        return receiver_firmware()

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