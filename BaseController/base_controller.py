import create_controllers

from BaseController import *
from typing import List

class BaseController:
    def __init__(self):
        self.controller: Controller
        self.firmware: Firmware

        self.controller = create_controllers.flight_computer_rev2_controller()
        self.firmware = Firmware(
            id=b"\x06",
            name="APPA",
            preset_frame_size=0,
            preset_file=""
        )