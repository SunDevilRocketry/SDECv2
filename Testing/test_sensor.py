from Sensor.sensor import *

def conv_fucntion(raw_data: float) -> float:
    return raw_data * 2.0 # Example conversion logic

sensor = Sensor(
    name = "Test Sensor",
    unit = "units",
    convert_data = conv_fucntion,
    low_byte_range = 4, # example byte range for accelerometer z
    upp_byte_range = 6
)

print(f"Sensor Name: {sensor.name}")
print(f"Sensor Unit: {sensor.unit}")
#convert data example call
print(f"Converted Data: {sensor.convert_data(10.0)}")  # Example raw data input
#data_dump example call, does not work because of missing serialObj, unsure how to handle that
print(f"Data Dump: {sensor.data_dump(b'\\x03', b'\\x01')}")  # Example opcode and subcommand

"""
    appa_sensor_sizes = {
    "raw": {
        "accX" :         2,
        "accY" :         2,
        "accZ" :         2,
        "gyroX":         2,
        "gyroY":         2,
        "gyroZ":         2,
        "magX" :         2,
        "magY" :         2,
        "magZ" :         2,
        "imut" :         2,
        "pres" :         4,
        "temp" :         4
        """