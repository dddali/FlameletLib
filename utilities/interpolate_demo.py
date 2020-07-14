from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 14
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fallback_to_cm'] = True
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

n_points = 5
num_grid = n_points * n_points
coord = np.linspace(0, 1, n_points)
x = []
y = []
z = []
# for i in range(n_points):
#     for j in range(n_points):
#         if i%2 == 0 and j%3 == 0:
#             # pass
#             continue
#         x.append(coord[i])
#         y.append(coord[j])
#         z.append( math.sin(x[-1]) + math.cos(y[-1]) )
rand_grid = np.random.rand(num_grid, 2)
for i in range(len(rand_grid)):
    x.append(rand_grid[i][0])
    y.append(rand_grid[i][1])
    z.append( math.sin(x[-1]) + math.cos(y[-1]) )

plt.figure(figsize=(8,16))
ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(313)
ax1.scatter(x, y, c=z,cmap='rainbow')
ax1.text(0,0.1,'Raw data')

##################### test
# f = interpolate.interp2d(x, y, z, kind='linear')
f = interpolate.Rbf(x,y,z)
points = [[x[i], y[i]] for i in range(len(x))]
n_points = 400
num_grid = n_points * n_points
coord = np.linspace(0, 1, n_points)
x = np.zeros(num_grid)
y = np.zeros(num_grid)
z = np.zeros(num_grid)
z_exact = np.zeros(num_grid)
for i in range(n_points):
    for j in range(n_points):
        x[i * n_points + j] = coord[i]
        y[i * n_points + j] = coord[j]
        z[i * n_points + j] = f(x[i * n_points + j], y[i * n_points + j])
        z_exact[i * n_points + j] = math.sin(x[i * n_points + j]) + math.cos(y[i * n_points + j])

# new_points = [[x[i], y[i]] for i in range(len(x))]
# z = interpolate.griddata(points, z, new_points)

ax2.scatter(x, y, c=z,cmap='rainbow')
ax2.text(0.0,0.1,'Interpolated')
ax3.scatter(x, y, c=z_exact,cmap='rainbow')
ax3.text(0.0,0.1,'Exact')
plt.tight_layout()
plt.show()
