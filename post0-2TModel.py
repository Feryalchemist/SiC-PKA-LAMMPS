#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 09:56:11 2022

@author: feryantama
"""

import sys
filename = sys.argv[1]

def readthermo(filename):
    with open(filename+'.log','r') as f:
        line = f.readlines()
        data = {'Step':[],'Temp':[],'E_pair':[],'Press':[],
                'KinEng':[],'Atoms':[],'Time':[]}
        for n, l in enumerate(line):
            if 'Per MPI rank' in l:
                keyword = ''; c = 3
                while keyword == '':
                    if 'Loop time' not in line[n+c]:
                        for m,k in enumerate(list(data.keys())):
                            data[k] += [float(line[n+c].split()[m])]
                        c += 1
                    else:
                        keyword = 'stop'
    return data

def readpost (filename):
    with open(filename+'.tab','r') as f:
        line = f.readlines()
        data = {s.replace('"',''):[] for s in line[0].split()[1:]}
        for n, l in enumerate(line[1:],1):
            for m,k in enumerate(l.split()):
                data[list(data.keys())[m]] += [k]
            
    with open(filename+'.data','r') as f:
        line   = f.readlines()
        time   = []
        atom   = []
        n_atom = 0
        for n,l in enumerate(line):
            if "TIMESTEP" in l:
                time  += [int(line[n+1])]
            if "NUMBER OF ATOMS" in l:
                n_atom = int(line[n+1])
            if "ATOMS id" in l:
                D      = {s:[] for s in l.split()[2:]}
                for i in range(0,n_atom):
                    for m,d in enumerate(list(D.keys())):
                        D[d] += [line[n+i+1].split()[m]]
                atom  += [D]
    return(data,atom,time)

def Kinetic(atom):
    for i in range(0,len(atom)):        
        mass = []
        for t in atom[i]['type']:
            if int(t) == 1 or int(t) == 3:
                mass += [12.01115]
            else:
                mass += [28.086]
        atom[i]['mass'] = mass
        atom[i]['KE']   = [(0.5 * (float(v)*1e12/1e10)**2 * (m/1000)/6.023e23)/1.602e-19  
                           for v,m in zip(atom[i]['VelocityMagnitude'],mass)]
    return atom
    

def Deformation(atom):
    Count   = {'Si_i':[],'Si_v':[],'C_i':[],'C_v':[],
               'Si_C':[],'C_Si':[],'Si_B':[],'C_B':[]}
    Oc_list = []
    for i in range(0,len(atom)):
        for k in list(Count.keys()):
            Count[k] += [0]

        Oc_list += [list()]
        for j in range(len(atom[i]['id'])):
            Occupancy    = [int(atom[i]['Occupancy'+str(k)][j]) for k in range(1,5)]
            Oc_list[i]  += [Occupancy + [int(atom[i]['type'][j])]]
            if int(atom[i]['type'][j]) == 1: # Carbon
                # Vacancy or Interstitial
                if Occupancy[ int(atom[i]['type'][j])-1 ] == 0:
                    Count['C_v'][-1] += 1
                elif Occupancy[ int(atom[i]['type'][j])-1 ] > 1:
                    Count['C_i'][-1] += 1
        
                # Displaced to where
                if Occupancy[1]!=0:
                    Count['C_Si'][-1] += 1
                    if Occupancy[1] > 1:
                        Count['C_v'][-1]  += 1
                elif Occupancy[2] != 0 or Occupancy[3] != 0:
                    Count['C_B'][-1]  += 1
                
            elif int(atom[i]['type'][j]) == 2: # Silicon
                # Vacancy or Interstitial
                if Occupancy[ int(atom[i]['type'][j])-1 ] == 0:
                    Count['Si_v'][-1] += 1
                elif Occupancy[ int(atom[i]['type'][j])-1 ] > 1:
                    Count['Si_i'][-1] += 1
            
                # Displaced to where
                if Occupancy[0]!=0:
                    Count['Si_C'][-1] += 1
                    if Occupancy[0] > 1:
                        Count['Si_v'][-1]  += 1
                if Occupancy[2] != 0 or Occupancy[3] != 0:
                    Count['Si_B'][-1]  += 1
    return Count,Oc_list

data,atom,time      = readpost(filename) 
atom                = Kinetic(atom)               
Count,Occupancy     = Deformation(atom)
thermo              = readthermo(filename)

#import yaml
#with open("./Output/dump-2T-SiC-GW-1.yaml",'r') as file:
#    thermo = yaml.load(file,Loader=yaml.SafeLoader)

# ------------------------------------------------------------------
import matplotlib.pyplot as plt
plt.figure(dpi=300)
plt.title('Weigner-Seitz Defect by Type\n' + r'$_{T=300 K\ E_{PKA} = 1 keV}$')
for k in list(Count.keys()):
    plt.semilogx([0]+thermo['Time'],Count[k],label=k)
plt.legend(fontsize=9)
plt.xlim([19, 25])
plt.xlabel('time [ps]')
plt.ylabel('# of atoms')
plt.grid()

# ------------------------------------------------------------------
plt.figure(dpi=300)
plt.title('Temperature')
plt.semilogx(thermo['Time'],thermo['Temp'])
plt.legend(fontsize=9)
plt.xlim([5,10])
plt.xlabel('time [ps]')
plt.ylabel('Temperature [K]')
plt.grid()

# ------------------------------------------------------------------
plt.figure(dpi=300)
plt.title('Pressure')
plt.semilogx(thermo['Time'],thermo['Press'])
plt.legend(fontsize=9)
plt.xlim([5,10])
plt.xlabel('time [ps]')
plt.ylabel('Pressure [bar]')
plt.grid()
