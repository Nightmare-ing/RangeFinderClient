import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial

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


def update(frame):
    print(frame)
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


# ani = animation.FuncAnimation(fig, update, frames=1000, interval=0.1, repeat=False)
# plt.show()

# (points, ) = ax.plot([0], [0], animated=True)
plt.show(block=False)
plt.pause(0.1)
background = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(scat)
fig.canvas.blit(fig.bbox)

for i in range(10000):
    # print(dist, i)
    angle_data.append(np.random.normal(np.pi / 2, 1))
    dist_data.append(get_dist())
    fig.canvas.restore_region(background)
    scat.set_offsets(np.stack([angle_data, dist_data], axis=1))
    ax.draw_artist(scat)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()

    # scat.set_offsets(np.c_[angle_data, dist_data])
    # plt.pause(0.0000001)

plt.show()
