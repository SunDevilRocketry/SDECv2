from SDECv2.SerialController import SerialSentry, SerialObj, Comport

def test_serial_sentry():
    serial_sentry = SerialSentry()

    serial_controller = serial_sentry.open_comport()
    print("After creating a serial sentry and opening a comport: ")
    print(serial_sentry)
    print(serial_controller)
    print("------------------------------------------------------")

    serial_sentry.close_comport(serial_controller)
    print("After closing comport")
    print(serial_sentry)
    print(serial_controller)
    print("---------------------")

if __name__ == "__main__":
    test_serial_sentry()