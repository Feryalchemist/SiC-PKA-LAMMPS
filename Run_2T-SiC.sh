#!/bin/bash
# read-2TModel.py [index] [Energy-eV] [PKA-C/Si] [1/0-boolean thermostat]

# -------------------------------------------------
# ============ Si/C PKA 1 Simulation ==============

lmp -i Simulation_2T-SiC.init
 
python3 read2-2TModel.py --PKA_ID 33684 --Trial_ID 1 --E_PKA 1000 --Element C --Dir_index 1 3 5
mpiexec -np 4 lmp -i Simulation_2T-SiC.run

python3 read2-2TModel.py --PKA_ID 33680 --Trial_ID 2 --E_PKA 1000 --Element Si --Dir_index 1 3 5
mpiexec -np 4 lmp -i Simulation_2T-SiC.run

# -------------------------------------------------
# ========== Si/C PKA stats Simulation ============
# lmp -i Simulation_2T-SiC.init
# for t in {1..30}
# do
#    python3 read2-2TModel.py "$t01" 100000 C 1 
#    mpiexec -np 4 lmp -i Simulation_2T-SiC.run

#    python3 read2-2TModel.py "$t02" 100000 Si 1
#    mpiexec -np 4 lmp -i Simulation_2T-SiC.run

# done

