import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(layout='constrained', subplot_kw=dict(projection='polar'))

angle_data = np.random.normal(np.pi/2, 1, 30)
dist_data = np.random.uniform(0, 2.5, 30)

ax.scatter(angle_data, dist_data, c='r', marker='o', label='scanned points')

ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
ax.set_yticks(np.arange(0, 3, 0.5))
ax.set_title("Scan result of RangeFinder")
fig.legend(loc='outside lower center')
plt.show()
