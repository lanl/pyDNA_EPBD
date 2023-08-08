#!/usr/bin/sh

#SBATCH --job-name=qfactor
#SBATCH --output=/users/akabir/pyDNA_EPBD/logs/qfactor-%j.output
#SBATCH --error=/users/akabir/pyDNA_EPBD/logs/qfactor-%j.error
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


#SBATCH --array=0-13 # max 300(0-299) can be requested

## conda activate pydna_epbd_conda ## activate before running job
python pydna_epbd.run --config_filepath examples/qfactor/configs.txt
