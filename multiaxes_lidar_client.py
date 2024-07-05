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

        data_deque.append([x_data, y_data, z_data, dist])


def update_figure(frame):
    """
    function for updating the figure, called by FunctionAnimation
    :param frame: one frame for the figure
    :return: updated artists
    """
    global data
    data = np.array(data_deque).transpose()

    # update the color of each scattered point
    scat.set_color(cmap(norm(data[3])))
    scat._offsets3d = data[:3]
    bm.update()
    return [scat, ]


MAX_DIST = 7.0
NUM_POINTS_ON_VIEW = 500

ser = serial.Serial('/dev/tty.usbserial-13340', 3000000, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(
    projection='3d'))

data_deque = deque([[0.0, 0.0, 0.0, 0.0]] * NUM_POINTS_ON_VIEW,
                   maxlen=NUM_POINTS_ON_VIEW)
data = np.array(data_deque).transpose()
cmap = plt.colormaps['viridis']
norm = mcolors.Normalize(vmin=4, vmax=MAX_DIST)
scat = ax.scatter(data[0], data[1], data[2], c='r', marker='o',
                  edgecolor='none',
                  label='scanned points')
ax.set_xlim(6.0, 0.0)
ax.set_ylim(6.0, 0.0)
ax.set_zlim(-6.0, 6.0)
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
