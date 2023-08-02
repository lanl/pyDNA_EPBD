import os
import math

import configs.switches as switches
from simulation.input_reader import read_input_data
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
