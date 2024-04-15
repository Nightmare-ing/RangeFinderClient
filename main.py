import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial


def update(frame):
    angle_data.append(np.random.normal(np.pi / 2, 1))
    dist_data.append(get_dist())
    scat.set_offsets(np.stack([angle_data, dist_data], axis=1))
    return [scat,]


def get_dist():
    tof_raw_data = ser.read(4)
    tof_value = int.from_bytes(tof_raw_data[0:2]) + int.from_bytes(tof_raw_data[2:]) / 65536.0
    dist_per_clk = 300.0 / TDC_INNER_REF_CLK
    dist = dist_per_clk * tof_value / 2.0
    return dist


TDC_INNER_REF_CLK = 5  # in MHz

ser = serial.Serial('COM6', 115200, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='polar'))

angle_data = []
dist_data = []
scat = ax.scatter(angle_data, dist_data, c='r', marker='^', label='scanned points', animated=True)

ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
ax.set_yticks(np.arange(0, 4.0, 0.5))
ax.set_title("Scan result of RangeFinder")
fig.legend(loc='outside lower center')

ani = animation.FuncAnimation(fig, update, interval=0.1, frames=10000, repeat=False, blit=True)
plt.show()
