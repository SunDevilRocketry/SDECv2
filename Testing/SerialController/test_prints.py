from SerialController import SerialSentry, SerialObj, Comport

def test_prints():
    serial_sentry = SerialSentry()

    serial_connection = serial_sentry.open_serial("COM5", 9600, 1)

    print(serial_sentry.pretty_print())

    serial_sentry.close_serial(serial_connection)

if __name__ == "__main__":
    test_prints()