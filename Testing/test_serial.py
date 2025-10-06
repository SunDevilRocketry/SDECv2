from SerialController import SerialSentry, SerialObj, Comport

def test_serial():
    serial_connection = SerialObj()

    serial_connection.init_comport("COM3", 9600, 1)

    print("After init comport:")
    print(serial_connection)

    serial_connection.open_comport()

    print("After open comport")
    print(serial_connection)

    serial_connection.send_byte(b'\x00')

    print("After send byte")
    print(serial_connection)

    data = serial_connection.read_byte()
    print("Received byte {}".format(data))

    print("After read byte")
    print(serial_connection)

    serial_connection.close_comport()

    print("After close comport")
    print(serial_connection)

if __name__ == "__main__":
    test_serial()