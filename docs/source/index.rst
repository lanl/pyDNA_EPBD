.. pyDNA-EPBD documentation master file, created by
   sphinx-quickstart on Mon Jul 31 12:21:40 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyDNA-EPBD's documentation!
======================================
This repository corresponds to the article titled as **pyDNA-EPBD: A Python-based Implementation of the Extended Peyrard-Bishop-Dauxois Model for DNA Breathing Dynamics Simulation**.

|pic1|    |pic2|

.. |pic1| image:: ../../plots/p5_wtmt_avg_coord.png
   :width: 45%

.. |pic2| image:: ../../plots/p5_wtmt_avg_flip_1.414213562373096.png
   :width: 45%

**Background:** The dynamic behavior of DNA sequences, including local transient openings or *breathing* and *flipping*, is crucial in a wide range of biological processes and genomic disorders. However, accurate modeling and simulation of these phenomena, particularly for homogeneous and periodic DNA sequences, have remained a challenge due to the complex interplay of factors such as hydrogen bonding, electrostatic interactions, and base stacking.

**Results:** To address this, we have developed pyDNA-EPBD, a Python-based software tool that employs an extended version of the Peyrard–Bishop–Dauxois (EPBD) model. This extension integrates a sequence-dependent stacking term, enabling a more precise description of the DNA melting behavior for homogenous and periodic sequences. Through the use of a Monte Carlo Markov Chain (MCMC) approach, pyDNA-EPBD simulates DNA dynamics and generates data on DNA breathing characteristics such as bubble coordinates and flipping.

Resources
========================================
* `Paper <https://tobeprovided>`_
* `Code <https://github.com/lanl/pyDNA_EPBD>`_
* `Analysis Notebooks <https://github.com/lanl/pyDNA_EPBD/tree/main/analysis>`_
* `Utility of ML models <https://github.com/lanl/pyDNA_EPBD/tree/main/models>`


Installation
========================================
.. code-block:: shell
      
      git clone https://github.com/lanl/pyDNA_EPBD.git
      cd pyDNA_EPBD
      conda create -c conda-forge --name pydnaepbd_pypy39_conda pypy python=3.9 -y
      conda activate pydnaepbd_pypy39_conda
      pip install -r requirements.txt
      
      # To remove the conda venv
      conda deactivate
      conda remove --name pydnaepbd_pypy39_conda --all -y

Prerequisites
========================================
To run the simulation:
   * joblib>=1.3.0
   * numpy>=1.25.1

To analyze:
   * scikit-learn>=1.3.0
   * scipy>=1.11.1
   * pandas>=2.0.3
   * matplotlib>=3.7.2
   * seaborn>=0.12.2

Example DNA sequences, Configurations and Switches
========================================================
*inputs/p5_seqs/p5_wt_mt.txt*

.. code-block:: console

      P5_wt GCGCGTGGCCATTTAGGGTATATATGGCCGAGTGAGCGAGCAGGATCTCCATTTTGACCGCGAAATTTGAACGGCGC
      P5_mt GCGCGTGGCCATTTAGGGTATATATGGCCGAGTGAGCGAGCAGGATCTCCGCTTTGACCGCGAAATTTGAACGGCGC

*inputs/chicoma_configs.txt*

.. code-block:: console
      
      IsFirstColumnId         Yes # Yes/No
      SequencesDir            inputs/p5_seqs/
      OutputsDir              outputs/
      SaveFull                No  # Yes/No. if No, the simulation will save the summary, No is space efficient.
      SaveRuntime             No  # Yes/No. if No, it will not write the runtime.
      Flanks                  None # flanks will be added to all the seq on both sides, 26 GCs, None will not add anything
      Temperature             310
      Iterations              100
      Preheating              50000
      StepsAfterPreheating    80000
      NNodes                  1 # Number of nodes to divide the sequences equally (--array in slurm script).

*pydna_epbd/configs/switches.py*

.. code-block:: python
      
      import os
      os.environ['BUBBLE_MONITOR'] = "True"
      os.environ['ENERGY_MONITOR'] = 'False'
      os.environ['COORD_MONITOR'] = "True"
      os.environ['FLIPPING_MONITOR'] = "False"
      os.environ['FLIPPING_MONITOR_VERBOSE'] = "True"
      os.environ['MELTING_AND_FRACTION_MONITOR'] = "False"
      os.environ['MELTING_AND_FRACTION_MANY_MONITOR'] = "False"


Example Usage
========================================
*python pydna_epbd/run.py*

.. code-block:: python
      
      import os
      import math
      import time
      import switch

      from input_reader import read_input_data
      from simulation.simulation_steps import run_sequences

      if __name__ == "__main__":
         """This runs the simulation."""
         job_idx = 0

         # array job
         if "SLURM_ARRAY_TASK_ID" in os.environ:
            job_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])

         # InputConfigs class object
         input_configs = read_input_data("inputs/chicoma_configs.txt")

         # dividing the input sequences to the nodes based on job-idx
         chunk_size = math.ceil(len(input_configs.sequences) / input_configs.n_nodes)
         sequence_chunks = [
            input_configs.sequences[x : x + chunk_size]
            for x in range(0, len(input_configs.sequences), chunk_size)
         ]
         sequences = sequence_chunks[job_idx]
         print(f"job_idx:{job_idx}, n_seqs:{len(sequences)}")

         run_sequences(sequences, input_configs)


How to Cite pyDNA-EPBD?
========================================
.. code-block:: console

      @MISC{Eren2021pyCPAPR,
         author = {M. E. {Eren} and J. S. {Moore} and E. {Skau} and M. {Bhattarai} and G. {Chennupati} and B. S. {Alexandrov}},
         title = {pyCP\_APR},
         year = {2021},
         publisher = {GitHub},
         journal = {GitHub repository},
         doi = {10.5281/zenodo.4840598},
         howpublished = {\url{https://github.com/lanl/pyCP\_APR}}
      }

Authors
========================================
- `Anowarul Kabir <mailto:akabir4@gmu.edu>`_: Computer Sciece, George Mason University
- `Manish Bhattarai <mailto:ceodspspectrum@lanl.gov>`_: Theoretical Division, Los Alamos National Laboratory
- `Kim Rasmussen <mailto:kor@lanl.gov>`_: Theoretical Division, Los Alamos National Laboratory
- `Amarda Shehu <mailto:ashehu@gmu.edu>`_: Computer Sciece, George Mason University
- `Anny Usheva <mailto:Anny Usheva@brown.edu>`_: Surgery, Rhode Island Hospital and Brown University
- `Alan Bishop <mailto:arb@lanl.gov>`_: Theoretical Division, Los Alamos National Laboratory
- `Boian S. Alexandrov <mailto:boian@lanl.gov>`_: Theoretical Division, Los Alamos National Laboratory

Acknowledgments
========================================


Copyright Notice
========================================


License
========================================


References
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
