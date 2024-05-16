import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque
import serial
import threading


def update(frame):
    scat.set_offsets(np.stack([angle_data, dist_data], axis=1))
    return [scat, ]


def get_dist():
    tof_raw_data = ser.read(4)
    tof_value = int.from_bytes(tof_raw_data[0:2]) + int.from_bytes(tof_raw_data[2:]) / 65536.0
    dist_per_clk = 300.0 / TDC_INNER_REF_CLK
    dist = dist_per_clk * tof_value / 2.0
    return dist


def read_data():
    global iterate_counter
    while True:
        angle_data.append(float(ANGLE_VALUES[iterate_counter % len(ANGLE_VALUES)]))
        dist_data.append(get_dist())
        iterate_counter += 1


TDC_INNER_REF_CLK = 5  # in MHz
MIRROR_ANGLE_LIMIT = 40.0 / 180.0 * np.pi  # in radians
MIRROR_FREQ = 80.0  # in Hz
MEASURE_FREQ = 16666.6  # in Hz
iterate_counter = 0

SAMPLE_VALUES = np.linspace(-np.sin(MIRROR_ANGLE_LIMIT), np.sin(MIRROR_ANGLE_LIMIT),  int(MEASURE_FREQ / MIRROR_FREQ))
ANGLE_VALUES = np.arcsin(SAMPLE_VALUES)

ser = serial.Serial('COM11', 921600, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='polar'))

angle_data = deque([0.0] * 300, maxlen=300)
dist_data = deque([0.0] * 300, maxlen=300)
scat = ax.scatter(angle_data, dist_data, c='r', marker='^', label='scanned points', animated=True)

ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
ax.set_yticks(np.arange(0.0, 1.5, 0.1))
ax.set_title("Scan result of RangeFinder")
fig.legend(loc='outside lower center')

read_data_thread = threading.Thread(target=read_data, daemon=True)
read_data_thread.start()

ani = animation.FuncAnimation(fig, update, interval=1, repeat=False, blit=True)
plt.show()
ser.close()
read_data_thread.join()
