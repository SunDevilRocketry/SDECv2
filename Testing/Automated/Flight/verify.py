import os
import time
import traceback
from pathlib import Path
import json
import csv

print("[verify] Common imports done")

from BaseController import Firmware, BaseController
from BaseController import create_controllers
from Parser import Parser, PresetConfig, DataBitmask, FeatureBitmask, create_configs
from SerialController import SerialSentry, SerialObj, Comport
from Testing import Tester

print("[verify] SDEC imports done")

sdec_comport = os.environ.get("SDEC_COMPORT")

# set up results asserter
tester = Tester()

print("[verify] Opening SerialObj")

# Set serial object
serial_connection = SerialObj()

# connect
try:
    print("[verify] Connecting")
    serial_connection.init_comport(sdec_comport, 921600, 5)
    serial_connection.open_comport()
    serial_connection.connect()

    # assert proper connection
    print("[verify] Asserting Connection Status")
    tester.assert_result(serial_connection.target.controller.id == b'\x05', "Check that connect completed successfully (HW Opcode).")
    tester.assert_result(serial_connection.target.firmware.id == b'\x06', "Check that connect completed successfully (FW Opcode).")

    # download the preset
    print("[verify] Preset Download")
    tmp_dir = Path("Testing/Automated/Flight/temp")
    tmp_dir.mkdir(exist_ok=True)
    tmp_preset = tmp_dir / "tmp_preset.json"
    appa_parser = Parser(
        preset_config=create_configs.appa_preset_config(),
        preset_data=None
    )
    appa_parser.download_preset(serial_connection, path=tmp_preset.resolve())
    downloaded = {}
    with open(tmp_preset.resolve(), 'r') as file:
        downloaded = json.load(file)
    oracle = {}
    with open("Testing/Automated/Flight/test_presets.json", 'r') as file:
        oracle = json.load(file)

    # Check presets
    print("[verify] Checking Presets")
    tester.assert_result(downloaded.get("Feature Bitmask") == oracle.get("Feature Bitmask"), "Feature Bitmasks Equivalent")
    tester.assert_result(downloaded.get("Data Bitmask") == oracle.get("Data Bitmask"), "Feature Bitmasks Equivalent")
    tester.assert_result(downloaded.get("Config Data") == oracle.get("Config Data"), "Config Data Equivalent")
    
    # Flash Extract
    print("[verify] Flash Extract")
    extract_results = tmp_dir / "extract_results.json"
    extract_preset = tmp_dir / "extract_preset.json"
    appa_parser.flash_extract(serial_connection, preset_path=extract_preset.resolve(), data_path=extract_results.resolve())

    flash_data = []
    with open(extract_results.resolve(), "r") as f:
        reader = csv.reader(f)
        for row in reader:
            flash_data.append(row)
    flash_preset = {}
    with open(extract_preset.resolve(), "r") as f:
        flash_preset = json.load(f)

    # Verify extracted preset matches downloaded
    print("[verify] Verifying extract")
    tester.assert_result(flash_preset == downloaded, "Flash extract data matches downloaded preset.")

    # Verify frame sizes match
    # (row 0 is header row)
    tester.assert_result(flash_data[1][0] == '1', "First save bit present in extracted data.")
    tester.assert_result(flash_data[2][0] == '1', "Second save bit present in extracted data.")

    # Finish test
    print("[verify] Finalizing Test")
    time.sleep(1)
except Exception as e:
    print("A fatal error occurred during the test.")
    print(e)
    traceback.print_exc()
    tester.assert_result(False, "A fatal error occurred during execution. See the log for more details.")
except KeyboardInterrupt as e:
    pass
finally:
    try:
        serial_connection.close_comport()
    except Exception:
        pass
    script_dir = Path(__file__).parent.resolve()
    tester.write_results(str(script_dir), "verify.results")