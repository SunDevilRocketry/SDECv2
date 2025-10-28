import create_controllers

from BaseController import *
from typing import List

class BaseController:
    def __init__(self):
        self.controllers: List[Controller] = []
        self.firmwares: List[Firmware] = [Firmware(
            id=b"\x06",
            name="APPA",
            preset_frame_size=0,
            preset_file=""
        )]

        self.controllers.append(create_controllers.flight_computer_rev2_controller())