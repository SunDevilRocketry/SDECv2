# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .controller import Controller
from .firmware import Firmware
from .base_sensor import BaseSensor
from typing import List, Callable

class BaseController:
    """
    Base controller for managing firmware and sensors.
    Provides methods to interact with the controller and firmware.
    """

    def __init__(self, controller: Controller, firmware: Firmware):
        """
        Initialize the base controller with a controller and firmware.

        Args:
            controller (Controller): The controller (hardware) instance.
            firmware (Firmware): The firmware instance.
        """
        self.controller: Controller = controller
        self.firmware: Firmware = firmware

    def __str__(self):
        """
        Return a string representation of the base controller.

        Returns:
            str: String representation of the controller and firmware.
        """
        return (
            "Base Controller:{" + 
            f"\n{self.firmware}" +
            f"\n{self.controller}" +
            "\n}"
        )