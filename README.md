# SiC-PKA-LAMMPS

This repository contains Lammps simulation to simulate radiation damage in SiC-3C. The simulation will perform a PKA simulation by giving velocity to the atom near the center with Miller direction index <1 3 5>. This atom could be C or Si, but in the same C centered lattice. The simulation is simply a reconstruction of [this works](https://doi.org/10.1016/j.nme.2021.100957) but with Gao-Weber potential instead of Tersoff. The potentials are available on Lammps [github page](https://github.com/lammps/lammps/tree/develop/potentials). 

The simulation can be started by running "Run_2T-SiC.sh". It simply start the geometry initiation using .init file then it runs "read2-2TModel.py" to establish the thermostat layer from created geometry and set up PKA to .run file. .run file will perform the simulation and the data could be post-processed using OVITO. The "post0-2TModel.py" is a post processing file  to calculate combination of 4 type of particle sites occupancy and calculate their kinetic energy. However, this file is an independent post processing file, not python script for OVITO. Moreover, it still in development and not useful at the moment, especially in particle sites occupancy sorting function.

Read More :
1. [Molecular dynamics simulation of displacement cascades in cubic silicon carbide](https://doi.org/10.1016/j.nme.2021.100957)
2. [Molecular dynamics simulation of damage cascade creation in SiC/composites containing SiC/graphite interface](http://dx.doi.org/10.1016/j.nimb.2013.02.036)
3. [Electronic stopping in molecular dynamics simulations of cascades in 3C-SiC](https://doi.org/10.1016/j.jnucmat.2020.152371)
4. [MD simulation of two-temperature model in ion irradiation of 3C-SiC:Effects of electronic and nuclear stopping coupling, ion energy and crystal orientation](https://doi.org/10.1016/j.jnucmat.2021.153313)
