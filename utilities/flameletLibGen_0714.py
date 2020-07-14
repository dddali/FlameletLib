#!/home/xzhang/Computation/miniconda3/envs/spam/bin/python
# Wed Jul  1 20:48:18 CST 2020
import os
import cantera as ct
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from scipy import interpolate
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 16
mpl.rcParams['mathtext.fontset'] = 'stix'


########################################################
P0 = 101325.0  # constant pressure
HMAX = 1893.979337
HMIN = -5107190.788963
num_points = 51
########################################################

ctifile = input(
        'CTI FILE:  '
        '  Kerosene_122.cti'
        '  Ethanol_31.cti'
        '  POLIMI231.cti'
        '  Heptane0.cti\n')
gas = ct.Solution(ctifile)
data_directory = 'tables'  # output dir
if not os.path.exists(data_directory):
    os.makedirs(data_directory)


speciesNames = gas.species_names  # each species
nsp = len(speciesNames)  # number of species
molW = gas.molecular_weights  # molecular weights of each species
# first line
names = []
xIndex = -1
uIndex = -1
TIndex = -1
COIndex = -1
CO2Index = -1
H2Index = -1
H2OIndex = -1
ARIndex = -1
for filename in os.listdir():
    if filename.endswith('.csv'):
        with open(filename) as fi:
            line0 = fi.readline()
            names = [x.strip() for x in line0.split(',')]
        for i in range(len(names)):
            if names[i] == 'z' or names[i] == 'z (m)' or names[i] == 'x' or names[i] == 'x (m)':
                xIndex = i
            elif names[i] == 'u' or names[i] == 'u (m/s)':
                uIndex = i
            elif names[i] == 'T' or names[i] == 'T (K)':
                TIndex = i
            elif names[i] == 'CO':
                COIndex = i
                continue
            elif names[i] == 'CO2':
                CO2Index = i
                continue
            elif names[i] == 'H2':
                H2Index = i
                continue
            elif names[i] == 'H2O':
                H2OIndex = i
                continue
            elif names[i] == 'AR':
                ARIndex = i
                continue
        break  # only read one file

class TableLine(object):
    def __init__(self, Yc=0, h=0, omegaYc=0, T=0, Y=[]):
        self.Yc = Yc
        self.h = h
        self.omegaYc = omegaYc
        self.T = T
        self.Y = Y.copy()
    def __str__(self):
        s = [str(self.Yc), str(self.h), str(self.omegaYc), str(self.T)]
        s.extend([str(x) for x in self.Y])
        return ','.join(s)
    def __eq__(self, other):
        if not isinstance(other, TableLine):
            raise TypeError('TableLine')
        if (abs(self.Yc - other.Yc) < 1e-8) and (abs(self.h - other.h) < 1e-6):
            return True
        else:
            return False

table_map = {}
list_Z = []
for i in range(0,40):
    Z = i / 200.0
    list_Z.append(Z)
    table_map[Z] = []
for i in range(20,101):
    Z = i / 100.0
    list_Z.append(Z)
    table_map[Z] = []


n = 0  # count
for filename in os.listdir():
    if filename.endswith('.csv'):
        n += 1
        dataReaction = np.loadtxt(filename[:-4]+'-reaction', delimiter=',', skiprows=1).T  # reaction source
        data1orig = np.loadtxt(filename, delimiter=',', skiprows=1)
        data1 = np.transpose(data1orig)

        T = data1[TIndex]
        YAR = data1[ARIndex]
        YARO = max(YAR[-1], YAR[0])
        Z = (YAR - YARO) / (0.0-YARO)
        Yc = data1[H2OIndex] + data1[CO2Index]

        for i in range(len(data1)):
            if names[i] == speciesNames[0]:
                speciesStart = i

        # Calculate omegaYc
        omegaYc = dataReaction[CO2Index - speciesStart + 2] + dataReaction[H2OIndex - speciesStart + 2]
        Y = []
        h = np.zeros(len(Yc))
        for i in range(len(Yc)):
            Y = data1orig[i][speciesStart::].copy()
            gas.TPY = (T[i], P0, Y)
            h[i] = gas.enthalpy_mass

        for i in range(1, len(Z)):
            z0 = Z[i-1]
            z1 = Z[i]
            for z_pos in range(len(list_Z)):
                if (list_Z[z_pos] >= z0 and list_Z[z_pos] <= z1) or (list_Z[z_pos] <= z0 and list_Z[z_pos] >= z1):
                    lw = 0.5
                    uw = 0.5
                    if abs(z1 - z0) > 1e-10:
                        lw = (z1 - list_Z[z_pos]) / (z1 - z0)
                        uw = (list_Z[z_pos] - z0) / (z1 - z0)
                    c0 = Yc[i-1] * lw + Yc[i] * uw
                    h0 = h[i-1] * lw + h[i] * uw
                    omg0 = omegaYc[i-1] * lw + omegaYc[i] * uw
                    t0 = T[i-1] * lw + T[i] * uw
                    yi0 = data1orig[i-1][speciesStart::].copy()
                    yi1 = data1orig[i][speciesStart::].copy()
                    y0 = []
                    for k in range(len(yi0)):
                        y0.append(yi0[k] * lw + yi1[k] * uw)
                    new_line = TableLine(c0, h0, omg0, t0, y0)
                    lines_tmp = table_map[list_Z[z_pos]]

                    existed = False
                    for line in lines_tmp:
                        if line == new_line:
                            existed = True
                            break
                    if not existed:
                        lines_tmp.append(new_line)

def normalize(lines : list):
    YcMin = lines[0].Yc
    YcMax = lines[0].Yc
    hMin = lines[0].h
    hMax = lines[0].h
    for i in range(len(lines)):
        if lines[i].h <= hMin:
            hMin = lines[i].h
        if lines[i].Yc <= YcMin:
            YcMin = lines[i].Yc
        if lines[i].h >= hMax:
            hMax = lines[i].h
        if lines[i].Yc >= YcMax:
            YcMax = lines[i].Yc
    for i in range(len(lines)):
        lines[i].h = (lines[i].h - HMIN) / (HMAX - HMIN)
    return [YcMin, YcMax, hMin, hMax]

YAIR = {'O2' : 0.23197, 'N2' : 0.75425, 'AR' : 0.01378}
YFUELS = {
    'Ethanol_31.cti' : {'C2H5OH' : 1.0},
    'POLIMI231.cti'  : {'NC12H26' : 0.292, 'IC16H34' : 0.465, 'DECALIN' : 0.194, 'C7H8' : 0.049}
}


for Z in table_map.keys():
    if Z != 0.01:
        continue
    print('Z: ', Z)
    lines = table_map[Z]

    YcMin, YcMax, hMin, hMax = normalize(lines)
    print(YcMin, YcMax, hMin, hMax)

    # Yc = 0
    if (hMax - hMin) / (HMAX - HMIN) > 0.05:
        print('\tAdding mixing states...')
        mixing_composition = {}
        for key in YAIR.keys():
            mixing_composition[key] = YAIR[key] * (1.0 - Z)
        for key in YFUELS[ctifile].keys():
            mixing_composition[key] = YFUELS[ctifile][key] * Z
        dh_step = (hMax - hMin) / 10.0
        for i in range(11):
            htmp = hMin + dh_step * i
            try:
                gas.HPY = htmp, P0, mixing_composition
                h_norm = (htmp - HMIN) / (HMAX - HMIN)
                lines.append(TableLine(0.0, h_norm, 0, gas.T, gas.Y))
            except:
                pass

    C = np.linspace(0.0, 1.0, num_points)
    H = np.linspace(0.0, 1.0, num_points)

    C_points = np.zeros(num_points * num_points)
    H_points = np.zeros(num_points * num_points)
    omegaYc = np.zeros(num_points * num_points)
    T = np.zeros(num_points * num_points)
    Y = [np.zeros(num_points * num_points) for i in range(nsp)]

    xc = [l.Yc for l in lines]
    yh = [l.h for l in lines]
    zT = [l.T for l in lines]
    zOmega = [l.omegaYc for l in lines]
    zY = []
    for k in range(nsp):
        zY.append([l.Y[k] for l in lines])

    if len(xc) == 0:
        raise Exception('No interpolating points')
    elif len(xc) == 1:
        fOmega = lambda x,y : zOmega[0]
        fT = lambda x,y : zT[0]
        fY = []
        for k in range(nsp):
            fY.append(lambda x,y : zY[k][0])
    else:
        fOmega = interpolate.Rbf(xc,yh,zOmega,function='linear')
        fT = interpolate.Rbf(xc,yh,zT,function='linear',smooth=0)
        fY = []
        for k in range(nsp):
            fY.append(interpolate.Rbf(xc,yh,zY[k],function='linear',smooth=0))

    for i in range(num_points):
        for j in range(num_points):
            C_points[i * num_points + j] = C[i]
            H_points[i * num_points + j] = H[j]
            Yc_point = C[i] * (YcMax - YcMin) + YcMin
            h_point = ((H[j] * (hMax - hMin) + hMin) - HMIN) / (HMAX - HMIN)
            print(Yc_point, h_point)

            omegaYc[i * num_points + j] = fOmega(Yc_point, h_point)
            T[i * num_points + j] = min(3000.0, max(275, fT(Yc_point, h_point)))
            sum_Y = 0.0
            for k in range(nsp):
                Y[k][i * num_points + j] = min(1.0, max(0.0, fY[k](Yc_point, h_point)))
                sum_Y += Y[k][i * num_points + j]
            for k in range(nsp):
                Y[k][i * num_points + j] /= sum_Y

    plt.figure(figsize=(12,7))
    sc = plt.scatter(xc,yh,c=zT,cmap='rainbow')
    cbar = plt.colorbar(sc)
    cbar.set_label(r'$T$ $\mathrm{(K)}$')
    plt.xlabel(r'$Y_c^*$')
    plt.text(0,1.1,'Yc : %f ~ %f,  H : %f ~ %f'%(YcMin, YcMax, hMin, hMax))
    plt.ylabel(r'$H^*$')

    plt.figure(figsize=(12,7))
    sc = plt.scatter(C_points, H_points, c=T, cmap='rainbow')
    cbar = plt.colorbar(sc)
    cbar.set_label(r'$T$ $\mathrm{(K)}$')
    plt.text(0,1.1,'Yc : %f ~ %f,  H : %f ~ %f'%(YcMin, YcMax, hMin, hMax))
    plt.xlabel(r'$Y_c^*$')
    plt.ylabel(r'$H^*$')
    plt.show()

    filename2 = os.path.join(data_directory, 'Z-%.3f.data' % (Z))
    with open(filename2, 'w+') as f:
        line = '%f %f %f %f %f %d %d' % (Z, YcMin, YcMax, hMin, hMax, num_points, nsp)
        f.write(line+'\n')
        for i in range(num_points * num_points):
            line1 = ' '.join([str(x) for x in [C_points[i], H_points[i], omegaYc[i], T[i]]])
            Yi = [Y[k][i] for k in range(nsp)]
            line2 = ' '.join([str(x) for x in Yi])
            line = ' '.join([line1, line2])
            f.write(line + '\n')


filename2 = os.path.join(data_directory, 'config.txt')
with open(filename2, 'w+') as f:
    f.write(' '.join(['%.3f'%(x) for x in list_Z]))

