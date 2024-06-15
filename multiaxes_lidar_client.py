import serial
from data_receive import *
import matplotlib.pyplot as plt
from collections import deque
import threading
import matplotlib.animation as animation


def read_data():
    """
    thread function for pushing one frame data into the deque continuously
    """
    while True:
        one_frame_x, one_frame_y, one_frame_z = get_data(ser)
        x.append(one_frame_x)
        y.append(one_frame_y)
        z.append(one_frame_z)


def update_figure(frame):
    """
    function for updating the figure, called by FunctionAnimation
    :param frame: one frame for the figure
    :return: updated artists
    """
    scat.set_offsets(np.stack([x, y, z], axis=1))
    return [scat,]


ser = serial.Serial('/dev/tty.usbserial-13130', 3000000, timeout=1)
fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='3d'))

x = deque([0.0] * 500, maxlen=500)
y = deque([0.0] * 500, maxlen=500)
z = deque([0.0] * 500, maxlen=500)
scat = ax.scatter(x, y, z, c='r', marker='^', label='scanned points')

read_data_thread = threading.Thread(target=read_data(), daemon=True)
read_data_thread.start()

ani = animation.FuncAnimation(fig, update_figure(), interval=1,
                              repeat=False, blit=True)
plt.show()
read_data_thread.join()
ser.close()


