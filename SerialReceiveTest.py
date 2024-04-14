import serial

ser = serial.Serial('COM6', 115200, timeout=1)

while True:
    TOF_raw_data = ser.read(4)
    TOF_value = int.from_bytes(TOF_raw_data[0:2]) + int.from_bytes(TOF_raw_data[2:]) / 65536.0
    print(TOF_value)
