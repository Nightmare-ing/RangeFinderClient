import serial
from serial import Serial
import numpy as np


def get_data(ser: Serial):
    """
    retrieve one frame data from serial port
    :param ser: the serial port to read from
    :return: (angle from fast axis, angle from slow axis, dist)
    """
    while True:
        # Get the beginner of one data frame
        while (beginner := ser.read()) and beginner != bytes.fromhex(BEGIN_CHECK_CODE):
            pass

        data_frame = beginner + ser.read(7)
        if data_frame[-1:] == bytes.fromhex(END_CHECK_CODE):
            return process_data(data_frame)


def process_data(data_frame: bytes):
    """
    process one frame raw data
    :param data_frame: 8 bytes data containing two bytes angle data from
    fast axis, two bytes angle data from slow axis, and two bytes data of
    dist in float form
    :return: (angle from fast axis, angle from slow axis, dist)
    """
    fast_axis_angle = int.from_bytes(data_frame[1:3])
    slow_axis_angle = int.from_bytes(data_frame[3:5])
    dist = np.float16(data_frame[5:-1])
    return fast_axis_angle, slow_axis_angle, dist


BEGIN_CHECK_CODE = 'aa'  # start check code in hexadecimal
END_CHECK_CODE = 'aa'  # end check code in hexadecimal

ser = serial.Serial('/dev/tty.usbserial-13130', 3000000, timeout=1)
for _ in range(100):
    print(get_data(ser))

ser.close()
