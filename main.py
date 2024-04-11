import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='polar'))
ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
plt.show()
