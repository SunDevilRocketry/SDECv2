import os
import time
import traceback
from pathlib import Path

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Parser import Parser, PresetConfig, DataBitmask, FeatureBitmask, create_configs
from SerialController import SerialSentry, SerialObj, Comport
from Testing import Tester

sdec_comport = os.environ.get("SDEC_COMPORT")

# set up results asserter
tester = Tester()

# Set serial object
serial_connection = SerialObj()

# connect
try:
    serial_connection.init_comport(sdec_comport, 921600, 3)
    serial_connection.open_comport()
    serial_connection.connect()

    # assert proper connection
    tester.assert_result(serial_connection.target.controller.id == b'\x05', "Check that connect completed successfully (HW Opcode).")
    tester.assert_result(serial_connection.target.firmware.id == b'\x06', "Check that connect completed successfully (FW Opcode).")

    parser = Parser.upload_preset(serial_connection, path="Testing/Automated/Flight/test_presets.json")
    tester.assert_result(type(parser) == Parser, "The parser object was created successfully.")
    
    # give enough time to complete the serial transaction
    time.sleep(2)
except Exception as e:
    print("A fatal error occurred during the test.")
    print(e)
    traceback.print_exc()
    tester.assert_result(False, "A fatal error occurred during execution. See the log for more details.")
finally:
    try:
        serial_connection.close_comport()
    except Exception:
        pass
    script_dir = Path(__file__).parent.resolve()
    tester.write_results(str(script_dir), "setup.results")