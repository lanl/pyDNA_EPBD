import os
import math
import argparse

from pydna_epbd.input_reader import read_configurations
from pydna_epbd.simulation.simulation_steps import run_sequences


def parse_args():
    parser = argparse.ArgumentParser(description="This runs the simulation")
    parser.add_argument(
        "--config_filepath",
        type=str,
        required=True,
        help="The Configuration filepath.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    """This runs the simulation."""
    args = parse_args()

    job_idx = 0

    # array job
    if "SLURM_ARRAY_TASK_ID" in os.environ:
        job_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])

    input_configs = read_configurations(args.config_filepath)

    # dividing the input sequences to the nodes based on job-idx
    chunk_size = math.ceil(len(input_configs.sequences) / input_configs.n_nodes)
    sequence_chunks = [
        input_configs.sequences[x : x + chunk_size]
        for x in range(0, len(input_configs.sequences), chunk_size)
    ]
    sequences = sequence_chunks[job_idx]
    print(f"job_idx:{job_idx}, n_seqs:{len(sequences)}")

    run_sequences(sequences, input_configs)

# python pydna_epbd/run.py --config_filepath examples/p5/configs.txt
