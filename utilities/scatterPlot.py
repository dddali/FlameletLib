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
figs = (10,7)

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
    h = data1[2]
    omega = data1[3]
    T = data1[4]
    YSP = data1[5]


    # sc = plt.scatter(Z1,Yc,c=omega,cmap='rainbow', vmin=0, vmax=420)
    # sc = plt.scatter(Z1,Yc,c=T,cmap='rainbow',vmin=300,vmax=2200)
    sc = plt.scatter(Z1, Yc, c=YSP, cmap='rainbow')
# v = [300,500,1000,1500,2000,2300]
# cbar = plt.colorbar(sc,ticks=v)
cbar = plt.colorbar(sc)
# cbar.set_label(r'$T$ $\mathrm{(K)}$')
# cbar.set_label(r'$\omega_{Y_c}$ $\mathrm{(kg/m^3s)}$')
plt.xlim(0, 1.0)
plt.ylim(0,0.3)
plt.xlabel(r'$Z$ (-)')
plt.ylabel(r'$Y_c$ (-)')
plt.tight_layout()
plt.savefig("scatter_plot.png")
plt.show()
