#!/usr/bin/sh

#SBATCH --job-name=gcpbm
#SBATCH --output=/users/akabir/pyDNA_EPBD/logs/gcpbm-%j.output
#SBATCH --error=/users/akabir/pyDNA_EPBD/logs/gcpbm-%j.error
#SBATCH --mail-user=<akabir@lanl.gov>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=gpu 
#SBATCH --account=y23_unsupgan_g 
#SBATCH --cpus-per-task=64
#SBATCH --mem=16G
#SBATCH --time=12:00:00 ##HH:MM:SS

#SBATCH --array=0-299 # max 300(0-299) can be requested

## conda activate pydna_epbd_conda ## activate before running job
python pydna_epbd.run --config_filepath examples/gcpbm/configs.txt