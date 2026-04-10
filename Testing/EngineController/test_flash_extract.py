from EngineController import flash_extract, EngineControllerFlashFrame
from SerialController import SerialObj

def test_flash_extract():
    serial = SerialObj()
    serial.init_comport("COM3", 921600, 30)
    serial.open_comport()

    frames = flash_extract(serial, store_data=True)

    print(f"Total frames: {len(frames)}")
    if frames:
        first = frames[0]
        print(f"First frame — timestamp: {first.timestamp_ms} ms")
        for name, value in first.sensor_readings.items():
            print(f"  {name}: {value:.3f}")

    serial.close_comport()

if __name__ == "__main__":
    test_flash_extract()
