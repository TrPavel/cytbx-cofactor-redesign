#!/bin/bash

#SBATCH --job-name=cytbx_znh
#SBATCH --account=BIOC033864
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-0:0:00
#SBATCH --mem=5GB
#SBATCH --array=1-20

srun rosetta_scripts.serialization.linuxgccrelease @cytbx_znh_flags.txt \
-out:suffix $SLURM_ARRAY_TASK_ID \
-out:prefix $SLURM_JOBID \
-out:file:silent struct_500_$SLURM_ARRAY_TASK_ID \
-out:path:all output


