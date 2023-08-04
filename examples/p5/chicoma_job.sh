#!/usr/bin/sh

#SBATCH --job-name=selex
#SBATCH --output=/users/akabir/pyDNA_EPBD/logs/selex-%j.output
#SBATCH --error=/users/akabir/pyDNA_EPBD/logs/selex-%j.error
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


##SBATCH --array=0-299 # max 300(0-299) can be requested

## conda activate pydna_epbd_conda ## activate before running job
python pydna_epbd/run.py --config_filepath examples/p5/configs.txt