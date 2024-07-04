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
    dist, all in uint16 type
    :return: (angle from fast axis, angle from slow axis, dist in m)
    """
    # print(data_frame)
    fast_axis_angle = (int.from_bytes(data_frame[1:2]) + int.from_bytes(data_frame[2:3]) * 256) / 4 / 4096 * 3.3
    slow_axis_angle = (int.from_bytes(data_frame[3:4]) + int.from_bytes(data_frame[4:5]) * 256) / 4 / 4096 * 3.3
    dist = int.from_bytes(data_frame[5:6]) + int.from_bytes(data_frame[6:7]) * 256

    fast_axis_angle = (fast_axis_angle - 1.65) / 2.475 * np.pi / 2 + np.pi / 4
    slow_axis_angle = (slow_axis_angle - 1.65) / 2.475 * np.pi / 2
    dist = dist / 100.0

    return fast_axis_angle, slow_axis_angle, dist


BEGIN_CHECK_CODE = 'aa'  # start check code in hexadecimal
END_CHECK_CODE = 'aa'  # end check code in hexadecimal

