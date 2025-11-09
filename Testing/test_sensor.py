from Sensor import Sensor
from SerialController import SerialSentry, SerialObj, Comport

def conv_fucntion(raw_data: float) -> float:
    return raw_data * 2.0 # Example conversion logic

serial_connection = SerialObj()

sensor = Sensor(
    name = "Test Sensor",
    unit = "units",
    convert_data = conv_fucntion,
    offset = 4, 
    size = 2,
    opcode = b'\x03' 
)

print(f"Sensor Name: {sensor.name}")
print(f"Sensor Unit: {sensor.unit}")
#convert data example call
print(f"Converted Data: {sensor.convert_data(10.0)}")  # Example raw data input

print(f"Data Dump: {sensor.data_dump(b'\x01', serial_connection)}")  # Example subcommand


#prototype making full list of sensor using dictionary from base controller just first three though and do those tests i have above
poll_codes = {
        b'\x00': Sensor("accX", "Accelerometer X", 2, int, "m/s/s"),
        b'\x01': Sensor("accY", "Accelerometer Y", 2, int, "m/s/s"),
        b'\x02': Sensor("accZ", "Accelerometer Z", 2, int, "m/s/s"),
        b'\x03': Sensor("gyroX", "Gyroscope X", 2, int, "deg/s"),
        b'\x04': Sensor("gyroY", "Gyroscope Y", 2, int, "deg/s"),
        b'\x05': Sensor("gyroZ", "Gyroscope Z", 2, int, "deg/s"),
        b'\x06': Sensor("magX", "Magnetometer X", 2, int, ""),
        b'\x07': Sensor("magY", "Magnetometer Y", 2, int, ""),
        b'\x08': Sensor("magZ", "Magnetometer Z", 2, int, ""),
        b'\x09': Sensor("imut", "IMU Die Temperature", 2, int, "deg C"), # Unused

        b'\x0A': Sensor("accXconv", "Pre-converted Accel X", 4, float, "m/s/s"),
        b'\x0B': Sensor("accYconv", "Pre-converted Accel Y", 4, float, "m/s/s"),
        b'\x0C': Sensor("accZconv", "Pre-converted Accel Z", 4, float, "m/s/s"),
        b'\x0D': Sensor("gyroXconv", "Pre-converted Gyro X", 4, float, "deg/s"),
        b'\x0E': Sensor("gyroYconv", "Pre-converted Gyro Y", 4, float, "deg/s"),
        b'\x0F': Sensor("gyroZconv", "Pre-converted Gyro Z", 4, float, "deg/s"),

        b'\x10': Sensor("rollDeg", "Roll Body Angle", 4, float, "deg"),
        b'\x11': Sensor("pitchDeg", "Pitch Body Angle", 4, float, "deg"),
        b'\x12': Sensor("rollRate", "Roll Body Rate", 4, float, "deg/s"),
        b'\x13': Sensor("pitchRate", "Pitch Body Rate", 4, float, "deg/s"),

        b'\x14': Sensor("velo", "Velocity", 4, float, "m/s"),
        b'\x15': Sensor("velo_x", "Velo X", 4, float, "m/s"),
        b'\x16': Sensor("velo_y", "Velo Y", 4, float, "m/s"),
        b'\x17': Sensor("velo_z", "Velo Z", 4, float, "m/s"),

        b'\x18': Sensor("pos", "Position", 4, float, "m"),
        b'\x19': Sensor("pres", "Barometric Pressure", 4, float, "kPa"),
        b'\x1A': Sensor("temp", "Barometric Temperature", 4, float, "C"),
        b'\x1B': Sensor("alt", "Barometric Altitude", 4, float, "m"),
        b'\x1C': Sensor("bvelo", "Barometric Velocity", 4, float, "m/s"),

        b'\x1D': Sensor("altg", "GPS Altitude (ft)", 4, float, "ft"),
        b'\x1E': Sensor("speedg", "GPS Speed (KmH)", 4, float, "km/h"),
        b'\x1F': Sensor("utc_time", "GPS UTC Time", 4, float, "s"),
        b'\x20': Sensor("long", "GPS Longitude (deg)", 4, float, "deg"),
        b'\x21': Sensor("lat", "GPS Latitude (deg)", 4, float, "deg"),

        b'\x22': Sensor("ns", "GPS North/South", 1, str, "N/S"),
        b'\x23': Sensor("ew", "GPS East/West", 1, str, "E/W"),
        b'\x24': Sensor("gll_s", "GPS GLL Status", 1, str, ""),
        b'\x25': Sensor("rmc_s", "GPS RMC Status", 1, str, "")
    }
#do for loop down here

#this for loop to test all sensors
#for sensor in poll_codes.values():
    
for i in range(3):  # Testing first three sensors
    sensor = list(poll_codes.values())[i] #confused on how the dictionary works, do i need to change sensor class?
    print(f"Testing Sensor: {sensor.name}")
    print(f"Unit: {sensor.unit}")
    print(f"Data Dump: {sensor.data_dump(b'\x01', serial_connection)}")  




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