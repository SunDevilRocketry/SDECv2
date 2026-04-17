from BaseController import create_controllers
from EngineController import (
    EngineState, ENGINE_STATE_NAMES,
    CONTROLLER_ID, CONTROLLER_NAME,
    get_state, telemetry_request,
)
from SerialController import SerialObj

def test_engine_controller():
    ec_rev5 = create_controllers.engine_controller_rev5_controller()

    print(f"Controller: {ec_rev5.name}")
    print(f"Controller ID: {ec_rev5.id}")
    print(f"Sensor frame size: {ec_rev5.sensor_frame_size} bytes")
    print()
    print(ec_rev5.get_formatted_poll_codes())

def test_get_state():
    serial = SerialObj()
    serial.init_comport("COM3", 921600, 5)
    serial.open_comport()

    state = get_state(serial)
    if state is not None:
        print(f"Engine state: {ENGINE_STATE_NAMES[state]}")
    else:
        print("Failed to get engine state")

    serial.close_comport()

def test_telemetry_request():
    serial = SerialObj()
    serial.init_comport("COM3", 921600, 5)
    serial.open_comport()

    data = telemetry_request(serial)
    if data is not None:
        print("Sensor readings:")
        for name, value in data.sensor_readings.items():
            print(f"  {name}: {value:.3f}")
        print("Valve states:")
        for name, state in data.valve_states.items():
            print(f"  {name}: {state}")
    else:
        print("Telemetry request failed")

    serial.close_comport()

if __name__ == "__main__":
    test_engine_controller()
