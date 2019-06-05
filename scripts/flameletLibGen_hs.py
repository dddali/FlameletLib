# Thu May 16 14:29:15 CST 2019
import os
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

p = 101325.0

data_directory = 'tables/'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

numLoop = int( input('Enter loop numer\n> ') )
fuelType = input('1:\tJet-A\n2:\tnc12h26\n3:\tC2H5OH\n> ')
if fuelType=='1':
    gas = ct.Solution("KEROSENE_CRECK231.cti")
    fuel = ['NC12H26','IC16H34','DECALIN','C7H8']
    Y_f = np.array([0.29152, 0.465052, 0.19402, 0.04941])
elif fuelType=='2':
    gas = ct.Solution("nDodecane_CRECK.cti")
    fuel = ['NC12H26']
    Y_f = np.array([1.0])
elif fuelType=='3':
    gas = ct.Solution("Ethanol_31.cti")
    fuel = ['C2H5OH']
    Y_f = np.array([1.0])
else:
    raise Exception('Only support the above fuels')
speciesNames = gas.species_names
nsp = len(speciesNames)
molW = gas.molecular_weights

# Read first line
with open('initial_solution.csv') as fi:
    line = fi.readline()
    line = line.split(',')
    names = []
    for i in range(len(line)):
        names.append(line[i])
for i in range(len(names)):
    if names[i] == 'z' or names[i] == 'z (m)':
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

ax1 = plt.subplot(121)
ax2 = plt.subplot(122)
for n in range(0,numLoop+1,1):
    if n == 0:
        filename = 'initial_solution.csv'
    else:
        filename = 'strain_loop_{0:02d}.csv'.format(n)

    filename2 = data_directory + 'flameletTable_{:}.csv'.format(n)
    with open(filename2, 'w+') as fo:
        line = 'Z,Yc,omegaYc,T'
        for i in speciesNames:
            line += f',{i}'
        fo.write(line+'\n')

    data1orig = np.loadtxt(filename, delimiter=',', skiprows=1)
    data1 = np.transpose(data1orig)
    T = data1[TIndex]
    YAR = data1[ARIndex]
    YARO = max(YAR[-1], YAR[0])
    Z = (YAR - YARO) / (0.0-YARO)
    # Yc = data1[H2OIndex] + data1[H2Index] + data1[CO2Index] + data1[COIndex]

    for i in range(len(data1)):
        if names[i] == speciesNames[0]:
            speciesStart = i

    # Calculate omegaYc
    Y = []
    omegaYc = np.zeros(len(Z))
    Yc = np.zeros(len(Z))
    for i in range(len(Z)):
        Y = data1orig[i][speciesStart::]
        gas.TPY = (T[i], p, Y)
        omegaYc[i] = np.dot(gas.net_production_rates, gas.partial_molar_enthalpies)
        Yc[i] = gas.enthalpy_mass

    data2 = []
    data2.append(list(Z))
    data2.append(list(Yc))
    data2.append(list(omegaYc))
    ax1.plot(Z,Yc)
    ax2.plot(Z,omegaYc)
    data2.append(list(T))
    for i in range(len(data1)):
        if i >= speciesStart:
            data2.append(list(data1[i]))
        else:
            pass
    data2 = np.array(data2)
    data2 = np.transpose(data2)
    if Z[0] > 0.99:
        data2 = data2[::-1]
    else:
        pass
    with open(filename2,'a') as f:
        np.savetxt(f, data2, delimiter=',',fmt='%f')

plt.show()