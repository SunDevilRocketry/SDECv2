# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

from .controller import Controller
from .firmware import Firmware
from .base_sensor import BaseSensor
from typing import List, Callable

class BaseController:
    def __init__(self, controller: Controller, firmware: Firmware):
        self.controller: Controller = controller
        self.firmware: Firmware = firmware

    def __str__(self):
        return (
            "Base Controller:{" + 
            "\n{}".format(self.firmware) +
            "\n{}".format(self.controller) +
            "\n}"
        )