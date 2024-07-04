import numpy as np
import serial
import threading
from collections import deque

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from BlitManager import *
from data_receive import *


def read_data():
    """
    thread function for pushing one frame data into the deque continuously
    """
    global i
    while True:
        # fast_axis_angle, slow_axis_angle, dist = get_data(ser)
        fast_axis_angle = np.pi / 4.0
        slow_axis_angle = np.pi / 4.0
        dist = (i + 1) / 1000.0
        i = (i + 1) % 2000

        # if the distance is larger than MAX_DIST, abandon this data
        if dist > MAX_DIST:
            continue

        x_data = 1.0
        y_data = 1.0
        z_data = i / 10.0
        i = (i + 1) % 10
        # print(x_data, y_data, z_data)
        colors.append(cmap(norm(z_data)))
        x.append(x_data)
        y.append(y_data)
        z.append(z_data)
        # print(dist)


def update_figure(frame):
    """
    function for updating the figure, called by FunctionAnimation
    :param frame: one frame for the figure
    :return: updated artists
    """
    fast_axis_angle = np.random.uniform(0.0, 2*np.pi)
    slow_axis_angle = np.random.uniform(0.0, np.pi/2.0)
    dist = np.random.uniform(0.0, MAX_DIST)

    x_data = dist * np.cos(slow_axis_angle) * np.sin(fast_axis_angle)
    y_data = dist * np.cos(slow_axis_angle) * np.cos(fast_axis_angle)
    z_data = dist * np.sin(slow_axis_angle)
    colors.append(cmap(norm(z_data)))
    x.append(x_data)
    y.append(y_data)
    z.append(z_data)

    scat.set_color(colors)  # update the color of each scattered point
    scat._offsets3d = (x, y, z)
    bm.update()
    return [scat, ]


MAX_DIST = 2.0
i = 1

# ser = serial.Serial('/dev/tty.usbserial-1310', 3000000, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(
    projection='3d'))

x = deque([0.0] * 100, maxlen=100)
y = deque([0.0] * 100, maxlen=100)
z = deque([0.0] * 100, maxlen=100)
cmap = plt.colormaps['viridis']
norm = mcolors.Normalize(vmin=0, vmax=MAX_DIST)
colors = deque([cmap(0.0)] * 100, maxlen=100)
scat = ax.scatter(x, y, z, c=colors, marker='o', edgecolor='none',
                  label='scanned points')
ax.set_xlim(2.0, 0.0)
ax.set_ylim(2.0, 0.0)
ax.set_zlim(-2.0, 2.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=20, azim=45)

bm = BlitManager(fig.canvas, [scat, ])

# read_data_thread = threading.Thread(target=read_data, daemon=True)
# read_data_thread.start()

ani = animation.FuncAnimation(fig, update_figure, interval=1,
                              repeat=False)
plt.show()
# read_data_thread.join()
# ser.close()
