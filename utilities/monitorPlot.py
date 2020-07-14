import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 16
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['font.style'] = 'normal'
# mpl.rcParams['font.serif'] = 'DejaVu Serif'
# mpl.rcParams['font.serif'] = 'Georgia'
# mpl.rcParams['font.serif'] = 'Times New Roman'
# mpl.rcParams['text.usetex'] = True
mpl.rcParams['mathtext.fontset'] = 'stix'
# mpl.rcParams['mathtext.fallback_to_cm'] = True
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight'

# print("Enter file names:")
# filename = []
# while True:
#     name_input = input('> ')
#     if name_input == '':
#         break
#     else:
#         filename.append(name_input)
need_save = False
if input('Need save figures? 1 (yes) 0 (no)') == '1':
    need_save = True
else:
    pass

filename = 'monitor.csv'
fig, ax = plt.subplots(figsize=(9,5))
data = np.loadtxt(filename,delimiter=',',skiprows=1)
data = np.transpose(data)
data[0] -= data[0][0]
ax.plot(data[0], data[1], c='k', label='T max')
# ax.set_title(r'Temperature evolution with increasing strain rate')
# ax.set_title(r'Temperature evolution with increasing strain rate')
ax.legend()
diff = max(data[0]) - min(data[0])
ax.set_xlim(data[0][0], data[0][-1] + 0.05*diff)
# ax.set_ylim(280,2000)
ax.set_xlabel(r'Time $\mathrm{(s)}$')
ax.set_ylabel(r'Temperature $\mathrm{(K)}$')
plt.tight_layout()
if need_save:
    plt.savefig('mon_T.png', dpi=500, bbox_inches='tight')
plt.show()

fig2, ax2 = plt.subplots(figsize=(12,8))
ax2.plot(data[0],data[2],c='k',label='OH max')
ax.set_xlim(data[0][0], data[0][-1])
ax2.set_xlabel(r'$t$ $\mathrm{(s)}$')
ax2.set_ylabel(r'$Y$ $\mathrm{(-)}$')
ax2.legend()
plt.show()

fig3, ax3 = plt.subplots(figsize=(12,8))
ax3.plot(data[0],data[3],label='HCO max')
ax.set_xlim(data[0][0], data[0][-1])
ax3.set_xlabel(r'$t$ $\mathrm{(s)}$')
ax3.set_ylabel(r'$Y$ $\mathrm{(-)}$')
ax3.legend()
plt.show()
