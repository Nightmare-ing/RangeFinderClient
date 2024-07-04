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
    global data
    while True:
        fast_axis_angle, slow_axis_angle, dist = get_data(ser)
        # fast_axis_angle = np.random.uniform(0.0, 2 * np.pi)
        # slow_axis_angle = np.random.uniform(0.0, np.pi / 2.0)
        # dist = np.random.uniform(0.0, MAX_DIST)

        # if the distance is larger than MAX_DIST, abandon this data
        if dist > MAX_DIST:
            continue

        x_data = dist * np.cos(slow_axis_angle) * np.sin(fast_axis_angle)
        y_data = dist * np.cos(slow_axis_angle) * np.cos(fast_axis_angle)
        z_data = dist * np.sin(slow_axis_angle)

        colors.append(dist)
        x.append(x_data)
        y.append(y_data)
        z.append(z_data)


def update_figure(frame):
    """
    function for updating the figure, called by FunctionAnimation
    :param frame: one frame for the figure
    :return: updated artists
    """
    global data
    data = np.vstack([np.array(x), np.array(y), np.array(z), np.array(colors)])

    scat.set_color(cmap(norm(data[3])))  # update the color of each scattered
    # point
    scat._offsets3d = data[:3]
    bm.update()
    return [scat, ]


MAX_DIST = 2.0
NUM_POINTS_ON_VIEW = 100

ser = serial.Serial('/dev/tty.usbserial-1310', 3000000, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(
    projection='3d'))

x = deque([0.0] * NUM_POINTS_ON_VIEW, maxlen=NUM_POINTS_ON_VIEW)
y = deque([0.0] * NUM_POINTS_ON_VIEW, maxlen=NUM_POINTS_ON_VIEW)
z = deque([0.0] * NUM_POINTS_ON_VIEW, maxlen=NUM_POINTS_ON_VIEW)
data = np.zeros((4, NUM_POINTS_ON_VIEW))
colors = deque([0.0] * NUM_POINTS_ON_VIEW, maxlen=NUM_POINTS_ON_VIEW)
cmap = plt.colormaps['viridis']
norm = mcolors.Normalize(vmin=0, vmax=MAX_DIST)
scat = ax.scatter(x, y, z, c='r', marker='o', edgecolor='none',
                  label='scanned points')
ax.set_xlim(2.0, 0.0)
ax.set_ylim(2.0, 0.0)
ax.set_zlim(-2.0, 2.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=20, azim=45)

bm = BlitManager(fig.canvas, [scat, ])

read_data_thread = threading.Thread(target=read_data, daemon=True)
read_data_thread.start()

ani = animation.FuncAnimation(fig, update_figure, interval=1,
                              repeat=False)
plt.show()
read_data_thread.join()
ser.close()
