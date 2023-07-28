# pyDNA-EPBD
This repository corresponds to the article titled as "pyDNA-EPBD: A Python-based Implementation of the Extended Peyrard-Bishop-Dauxois Model for DNA Breathing Dynamics Simulation".


Avg coordinate profile     |  Avg coordinate profile 
:-------------------------:|:-------------------------:
![Alt text](plots/p5_wtmt_avg_coord.png)  |  ![Alt text](plots/p5_wtmt_avg_coord.png)


## Module setup instructions
Assuming the current directory is for creating the environment for pyDNA-EPBD simulation tool

```
conda create -c conda-forge -p pydnaepbd_pypy39_conda pypy python=3.9
conda activate /path/to/venv/pydnaepbd_pypy39_conda
pip install numpy # tested version: 1.25.1
pip install joblib # tested version: 1.3.1
```
Note that, pypy package is important for faster execution of the simulation. The following packages are needed for analysis:
```
pip install scikit-learn # tested version: 1.3.0
pip install pandas # tested version: 2.0.3
pip install matplotlib # tested version: 3.7.2
```


## Sample MCMC simulation run
Now activate the virtual environment and run the simulation.
Default setup runs the MCMC simulation on P5 wild- and mutant-promoter sequences. The corresponding configurations are described below. This can be changed to run the simulation on an arbitrary number of DNA sequences.
```
conda activate pydna_epbd_conda_release_venv
python run.py
```

## Configuration file structure
Must have following items (key, value) as space separated format. A sample configuration file (with slurm job file) with P5 wild- and mutant-promoter sequences are given in the inputs directory.

```
IsFirstColumnId         Yes # Yes/No. Whether or not the 1st column in the sequence containing file (s) is seq-id. Default Yes.
SequencesDir            path/to/sequences/dir/ # Can contain multiple files
OutputsDir              path/to/outputs/dir/
SaveFull                No  # Yes/No. If Yes, it will full outputs. No is space efficient.
SaveRuntime             No  # Yes/No. If Yes, it will write the runtime for each sequence.
Flanks                  None # Flanks will be added to all the seq on both sides, None will not add anything.
Temperature             310 # in Kelvin.
Iterations	            100 # Number of independent iterations with different initial conditions.
Preheating              50000 # Number of preheating steps.
StepsAfterPreheating	80000 # Number of post-preheating steps.
NNodes                  1 # Number of computing nodes available to divide the sequences (when running slurm job)
```

## The switches
The switches determine which monitor(s) to activate during the MCMC simulation. The value is "True" or "False" (with double quotation). To turn switches on/off, use `switch.py`. By default coodinate, flipping and bubble switches are on.

## Citation
If our pyDNA-EPBD simulation tool is found useful, we request to cite the relevant article:

```bibtex
@Article{}
```