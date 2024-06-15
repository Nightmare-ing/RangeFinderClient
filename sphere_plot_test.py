import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 创建一个图和3D坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 定义球的半径和角度网格
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

# 绘制球
ax.plot_surface(x, y, z, color='blue', alpha=0.5)

# 在球体上标记点
points = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, -1, -1)]
for point in points:
    ax.scatter(point[0], point[1], point[2], color='red')

# 设置坐标轴标签和标题
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Sphere Coordinates with Marked Points')

# 显示图形
plt.show()