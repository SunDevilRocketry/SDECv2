from SerialController import SerialSentry, SerialObj, Comport

def test_serial_sentry():
    serial_sentry = SerialSentry()

    serial_connection = serial_sentry.open_serial("COM3", 9600, 1)

    print("After open serial:")
    print(serial_sentry)
    print(serial_connection)

    print("Starting monitor")
    serial_sentry.monitor_serial_objs(time=10)

    serial_sentry.close_serial(serial_connection)

if __name__ == "__main__":
    test_serial_sentry()