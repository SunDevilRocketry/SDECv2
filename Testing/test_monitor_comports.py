from SDECv2.SerialController import SerialSentry, SerialObj, Comport
from time import sleep

def test_serial_sentry():
    serial_sentry = SerialSentry()

    serial_controller = serial_sentry.open_comport()
    print("After creating a serial sentry and opening a comport: ")
    print(serial_sentry)
    print(serial_controller)
    print("------------------------------------------------------")

    serial_sentry.monitor_comports(10)

    # for i in range(2):
    #     print(".", end="", flush=True)
    #     sleep(1)
    # print(".")
    sleep(2)

    print("Changing comport name to force monitor to observe a change")
    serial_sentry.comports[0].name = "Changed-Comport"

    # for i in range(10):
    #     print(".", end="", flush=True)
    #     sleep(1)
    # print(".")
    sleep(10)

    print("Manually fetching all observed changes: ")
    print(serial_sentry.get_changed_comports())
    print("----------------------------------------")

    print("After program has finished")
    print(serial_sentry)
    print(serial_controller)
    print("---------------------")

if __name__ == "__main__":
    test_serial_sentry()