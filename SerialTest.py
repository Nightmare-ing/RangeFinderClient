import serial

ser = serial.Serial('COM4', 115200, timeout=1)
ser.write(b'Hello World\n')
receive_data = ser.readline()
print("Receive data: ", receive_data)
ser.close()
