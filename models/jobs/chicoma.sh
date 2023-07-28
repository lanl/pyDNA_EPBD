#!/usr/bin/sh

#SBATCH --job-name=iss
#SBATCH --output=/users/akabir/pyDNA_EPBD/logs/iss-%j.output
#SBATCH --error=/users/akabir/pyDNA_EPBD/logs/iss-%j.error
#SBATCH --mail-user=<akabir@lanl.gov>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=standard
#SBATCH --account=t23_dna-epbd  
#SBATCH --mem=16G
#SBATCH --time=12:00:00

##SBATCH --array=0-8 # max 300(0-299) can be requested

## conda activate py311_conda ## activate before running job
python models/1_mls_with_bds.py
