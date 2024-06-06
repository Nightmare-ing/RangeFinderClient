import serial

ser = serial.Serial('/dev/tty.usbserial-13130', 3000000, timeout=1)
# ser.write(b'Hello World\n')
for _ in range(100):
    receive_data = ser.read(8)
    print("Receive data: ", receive_data)

ser.close()
