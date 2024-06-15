import numpy as np
import serial
from data_receive import *
import matplotlib.pyplot as plt
from collections import deque
import threading
import matplotlib.animation as animation
from BlitManager import *


def read_data():
    """
    thread function for pushing one frame data into the deque continuously
    """
    while True:
        fast_axis_angle, slow_axis_angle, dist = get_data(ser)
        # fast_axis_angle = np.random.uniform(0.0, 2*np.pi)
        # slow_axis_angle = np.random.uniform(0.0, np.pi/2.0)
        # dist = np.random.uniform(0.0, 5.0)

        x_data = dist * np.sin(slow_axis_angle) * np.cos(fast_axis_angle)
        y_data = dist * np.sin(slow_axis_angle) * np.sin(fast_axis_angle)
        z_data = dist * np.cos(slow_axis_angle)
        x.append(x_data)
        y.append(y_data)
        z.append(z_data)


def update_figure(frame):
    """
    function for updating the figure, called by FunctionAnimation
    :param frame: one frame for the figure
    :return: updated artists
    """
    scat._offsets3d = (x, y, z)
    bm.update()
    return [scat,]


ser = serial.Serial('/dev/tty.usbserial-13130', 3000000, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(
    projection='3d'))

x = deque([0.0] * 500, maxlen=500)
y = deque([0.0] * 500, maxlen=500)
z = deque([0.0] * 500, maxlen=500)
scat = ax.scatter(x, y, z, c='r', marker='^', label='scanned points')
ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-5.0, 5.0)
ax.set_zlim(-5.0, 5.0)

bm = BlitManager(fig.canvas, [scat,])

read_data_thread = threading.Thread(target=read_data, daemon=True)
read_data_thread.start()

ani = animation.FuncAnimation(fig, update_figure, interval=1,
                              repeat=False)
plt.show()
read_data_thread.join()
ser.close()


