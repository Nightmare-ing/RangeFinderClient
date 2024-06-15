import serial
from data_receive import *


ser = serial.Serial('/dev/tty.usbserial-13130', 3000000, timeout=1)
for _ in range(100):
    print(get_data(ser))

ser.close()
