import serial

TDC_INNER_REF_CLK = 5  # in MHz


def cal_dist(time):
    dist_per_clk = 300.0 / TDC_INNER_REF_CLK
    return dist_per_clk * time / 2.0


ser = serial.Serial('COM6', 115200, timeout=1)

count = 0
while True:
    count += 1
    TOF_raw_data = ser.read(4)
    TOF_value = int.from_bytes(TOF_raw_data[0:2]) + int.from_bytes(TOF_raw_data[2:]) / 65536.0
    dist = cal_dist(TOF_value)
    print(dist, count)
