from BaseController import BaseController, Firmware 
from BaseController import create_controllers

def test_base_controller():
    appa_firmware = Firmware(
        id=b"\x06",
        name="APPA",
        preset_frame_size=0,
        preset_file=""
    )

    flight_computer_rev2 = create_controllers.flight_computer_rev2_controller()

    appa_fc_rev2_base_controller = BaseController(flight_computer_rev2, appa_firmware)

    print(appa_fc_rev2_base_controller)

    print(appa_fc_rev2_base_controller.controller.get_formatted_poll_codes())

if __name__ == "__main__":
    test_base_controller()