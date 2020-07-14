import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
import matplotlib as mpl

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 14
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['savefig.dpi'] = 500
mpl.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.labelpad'] = 18
mks= ["o", "D", "d", "s", "p", "H", 0, 4, "<", "3",
      1, 5, ">", "4", 2, 6, "^", "2", 3, 7, "v", "1", "None", None, " ", ""]


fig = plt.figure(figsize=(9, 5))
ax = fig.add_subplot(111, projection='3d')

list_Z = ['0.000', '0.050', '0.100', '0.150', '0.200', '0.300', '0.400', '0.500', '0.600', '0.800', '1.000']
# with open('config.txt') as f:
#     list_Z = [x.strip() for x in f.readline().split(' ')]

for str_Z in list_Z:
    fname = 'Z-%s.data' % (str_Z)
    data = np.loadtxt(fname, skiprows=1, delimiter=' ').T
    sc = ax.scatter(float(str_Z), data[1], data[0], marker='D', c=data[3], vmin=273.15, vmax=2300, cmap='rainbow')

v = [300,500,1000,1500,2000]
cbar = plt.colorbar(sc,ticks=v)
# cbar = plt.colorbar(sc)
cbar.set_label(r'T (K)')
ax.set_xlabel(r'$Z$ (-)')
ax.set_ylabel(r'$H$ (-)')
ax.set_zlabel(r'$C$ (-)')
ax.tick_params(labelsize=14)
plt.tight_layout()
plt.savefig('3d.png',dpi=500)
plt.show()
