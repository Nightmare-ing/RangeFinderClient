from collections import deque

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation

from BlitManager import BlitManager


def update(frame):
    global i
    # fig.canvas.restore_region(background)  # Restore background

    # Update data
    x.append(1.0)
    y.append(i / 10.0)
    z.append(1.0)
    colors_single.append(i / 10.0)
    # data.append([1.0, i / 10.0, 1.0])
    data = np.vstack([np.array(x), np.array(y), np.array(z),
                      np.array(colors_single)])
    i = (i + 1) % 10

    sc._offsets3d = data[:3]  # Update positions
    sc.set_color(cmap(data[3]))  # Update colors

    bm.update()
    # ax.draw_artist(sc)  # Redraw just the scatter
    # fig.canvas.blit(ax.bbox)  # Blit just the updated area

i = 0
cmap = plt.colormaps['viridis']
norm = plt.Normalize(0, 1)
x = deque([1.0] * 10, maxlen=10)
y = deque([0.0] * 10, maxlen=10)
z = deque([1.0] * 10, maxlen=10)
# data = deque([[0.0, 0.0, 0.0]] * 10, maxlen=10)
colors = deque(cmap([0.0] * 10), maxlen=10)
colors_single = deque([0.0] * 10, maxlen=10)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
sc = ax.scatter(x, y, z, c=colors)
ax.set_xlim([0.75, 1.25])
ax.set_ylim([0, 1.5])
ax.set_zlim([0, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set up blitting
# fig.canvas.draw()
bm = BlitManager(fig.canvas, [sc, ])

ani = FuncAnimation(fig, update, frames=1000, interval=1000, repeat=False)

plt.show()