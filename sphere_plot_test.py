import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.random.standard_normal(100)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)
scatter = ax.scatter(x, y, z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.view_init(elev=20, azim=45)
ax.set_xlim([5, 0])
ax.set_ylim([5, 0])
ax.figure.canvas.draw()  # initial draw to setup the rendering context
background = ax.figure.canvas.copy_from_bbox(ax.figure.bbox)  # copy background
def update(frame):
    ax.figure.canvas.restore_region(background)  # restore the original background
    x = np.random.standard_normal(100)
    y = np.random.standard_normal(100)
    z = np.random.standard_normal(100)
    scatter._offsets3d = (x, y, z)  # update the data
    ax.draw_artist(scatter)  # redraw only the scatter
    ax.figure.canvas.blit(ax.figure.bbox)  # blit only the updated area
from matplotlib.animation import FuncAnimation

ani = FuncAnimation(fig, update, frames=np.arange(100), repeat=True)
plt.show()
