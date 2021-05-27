#!/bin/bash
#SBATCH --job-name=PI_MPI # Job name
#SBATCH --output=PI_MPI_%j.log # Log file name
#SBATCH --partition=compute # Use computing cluster
#SBATCH --mem=1gb # Job memory request
#SBATCH --nodes=8 # Number of computing nodes
#SBATCH --time=00:02:00 # Time limit HH:MM:SS

. /etc/profile.d/modules.sh

module load openmpi/2.1.2
module load python/3/mpi4py/3.0.0

/opt/openmpi-2.1.2/bin/mpirun python3 pi_mpi.py
