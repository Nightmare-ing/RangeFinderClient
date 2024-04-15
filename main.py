import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial

TDC_INNER_REF_CLK = 5  # in MHz

ser = serial.Serial('COM6', 115200, timeout=1)

fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='polar'))

angle_data = np.zeros((1000, 1))
dist_data = np.zeros((1000, 1))
scat = ax.scatter(angle_data, dist_data, c='r', marker='o', label='scanned points')

ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
ax.set_yticks(np.arange(0, 3.5, 0.5))
ax.set_title("Scan result of RangeFinder")
fig.legend(loc='outside lower center')


def update(frame):
    angle_data[frame] = np.random.normal(np.pi / 2, 1)
    dist_data[frame] = get_dist()
    data = np.stack([angle_data[:frame], dist_data[:frame]], axis=1)
    scat.set_offsets(data)
    return scat


def get_dist():
    tof_raw_data = ser.read(4)
    tof_value = int.from_bytes(tof_raw_data[0:2]) + int.from_bytes(tof_raw_data[2:]) / 65536.0
    dist_per_clk = 300.0 / TDC_INNER_REF_CLK
    dist = dist_per_clk * tof_value / 2.0
    print(dist)
    return dist


ani = animation.FuncAnimation(fig, update, interval=1, repeat=False)
plt.show()
