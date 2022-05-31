#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:55:07 2022

@author: feryantama
"""



import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--Trial_ID", help="ID of simulation", required=True, type=int)
parser.add_argument("--E_PKA",    help="PKA energy in eV", required=True, type=float)
parser.add_argument("--Element",  help="Element C/Si"    , required=True, type=str)
parser.add_argument("--Dir_index",help="Miller indices direction", required=True,
                    nargs="+")
parser.add_argument("--a",        help="lattice parameter in A",default=4.36, type=float)
parser.add_argument("--d",        help="lattice cubic supercell size",default=20, type=float)
parser.add_argument("--Thermostat_width", help="thermostat layer width in A",
                                  default=6, type=float)
parser.add_argument("--PKA_ID",   help="ID of PKA atom", type=int)
parser.add_argument("--Center_Radius",    help="center radius of random particle appear in center",
                                  default=(((4.36/2)**2)*3)**0.5,type=float)

args = parser.parse_args()


trial  = args.Trial_ID
E_PKA  = args.E_PKA     # in eV
Part   = args.Element   # particle type
Dir_id = [float(x) for x in args.Dir_index]

L = args.a    # Lattice Parameter
d = args.d    # Box supercell size (d x d x d)
s = args.Thermostat_width     # Fixed thermostat layer width
r = args.Center_Radius

# ------- Set Up Thermostat Layer --------
# ========================================
filename = "./Output/data.2T-SiC_Initial"
BBox     = [s,L*d-s]
with open(filename,'r') as f:
    line    = f.readlines()
    C_PKA   = []
    Si_PKA  = []
    N_atoms = int(line[2].split()[0])
    P_atoms = [0,0]; i=0
    while sum(P_atoms)==0:
        if 'Atoms # full' in line[i]:
            P_atoms = [i+2,i+N_atoms+1]
        i+=1
    for n,l in enumerate(line):
        if n>=P_atoms[0] and n<=P_atoms[1]:
            properties = l.split()
            x = float(properties[4])
            y = float(properties[5])
            z = float(properties[6])
            if ((x <= BBox[0] or x >= BBox[1] or
                 y <= BBox[0] or y >= BBox[1] or
                 z <= BBox[0] or z >= BBox[1])):
                if properties[2] == '1':
                    properties[2] = '3'
                else:
                    properties[2] = '4'
                    
            if ((x-L*d/2)**2 + (y-L*d/2)**2 + (z-L*d/2)**2 <= r**2):
                if properties[2] == '1':
                    C_PKA  += [int(properties[0])]
                elif properties[2] == '2':
                    Si_PKA += [int(properties[0])]
            
            line[n] = ' '.join(properties)+'\n'

filename = "./Output/data.2T-SiC_Modelled"
with open(filename,'w') as f:
    f.writelines(line)

# -------------- Set Up PKA --------------
# ========================================
import random
filename = "./Simulation_2T-SiC.run"
with open (filename,'r') as f:
    line     = f.readlines()    
    if args.PKA_ID:
        particle = [lists for lists in [[12.01115,C_PKA,'C'],[28.086,Si_PKA,'Si']] if Part in lists][0]
        ids      = args.PKA_ID
    else:
        particle = random.choice([[12.01115,C_PKA,'C'],[28.086,Si_PKA,'Si']])
        ids      = random.choice(particle[1])    
        
    v  = ((2*E_PKA*1.602e-19*6.023e23/(particle[0]/1000))**(0.5))*1e10/1e12
    vx,vy,vz = [x*v/((Dir_id[0]**2+Dir_id[1]**2+Dir_id[2]**2)**0.5) for x in Dir_id]
    
    for n,l in enumerate(line):
        if 'group           PKA id' in l:
            line[n] = 'group           PKA id {}\n'.format(int(ids)) 
        if 'velocity        PKA set ' in l:
            line[n] = 'velocity        PKA set {:.7f} {:.7f} {:.7f}\n'.format(vx,vy,vz)
        if 'variable        trial equal ' in l:
            line[n] = 'variable        trial equal {}\n'.format(int(trial))

with open(filename,'w') as f:
    f.writelines(line)

with open('./Output/Iteration-data.id',"a") as f:
    f.write('{}\t{}\t{}\t{:.7f}\t{:.7f}\t{:.7f}\t{:.7f}\n'.format(int(trial),int(ids),particle[2],v,vx,vy,vz))

