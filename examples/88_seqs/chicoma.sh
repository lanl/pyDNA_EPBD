#!/usr/bin/sh

#SBATCH --job-name=88_seqs
#SBATCH --output=/users/akabir/pyDNA_EPBD/logs/88_seqs-%j.output
#SBATCH --error=/users/akabir/pyDNA_EPBD/logs/88_seqs-%j.error
#SBATCH --mail-user=<akabir@lanl.gov>
#SBATCH --mail-type=BEGIN,END,FAIL

## gpu
##SBATCH --partition=gpu 
##SBATCH --account=y23_unsupgan_g 
##SBATCH --mem=16G

# cpu
#SBATCH --partition=standard
#SBATCH --account=t23_dna-epbd 
#SBATCH --mem=16G
#SBATCH --time=12:00:00 ##HH:MM:SS


#SBATCH --array=0-87 # max 300(0-299) can be requested

## conda activate pydna_epbd_conda ## activate before running job
python examples/88_seqs/run.py
