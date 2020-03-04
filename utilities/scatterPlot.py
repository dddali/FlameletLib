#Sat Dec 15 15:50:09 CST 2018
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Configurations
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 20
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.fallback_to_cm'] = True
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'
figs = (13,9)

# Input file names
print("Enter file names:")
filename = []
while True:
    name_input = input('> ')
    if name_input == '':
        break
    else:
        filename.append(name_input)


plt.figure(figsize=figs)
for ic,filename1 in enumerate(filename):
    data1 = np.loadtxt(filename1,delimiter=',',skiprows=1)
    data1 = np.transpose(data1)
    Z1 = data1[0]
    Yc = data1[1]

    sc = plt.scatter(Z1,Yc,c=data1[4],cmap='rainbow')
v = [300,500,1000,1500,2000,2300]
cbar = plt.colorbar(sc,ticks=v)
cbar.set_label(r'$T$ $\mathrm{(K)}$')
# plt.xlim(0,0.2)
# plt.ylim(0,0.3)
plt.xlabel(r'$Z$ (-)')
plt.ylabel(r'$Y_c$ (-)')
plt.tight_layout()
plt.show()
plt.savefig("scatter_plot.png")
