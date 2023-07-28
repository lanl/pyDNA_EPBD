import sys
sys.path.append("../pyDNA_EPBD")

import math
import os
import switch
# from selex.input_reader import read_input_data
from input_reader import read_input_data
from simulation.simulation_steps import run_sequences


if __name__ == "__main__":
    job_idx = 0

    # array job
    if "SLURM_ARRAY_TASK_ID" in os.environ:
        job_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])

    input_configs = read_input_data("examples/selex/chicoma.txt")

    # dividing the input sequences to the nodes based on job-idx
    chunk_size = math.ceil(len(input_configs.sequences) / input_configs.n_nodes)
    sequence_chunks = [input_configs.sequences[x:x+chunk_size] for x in range(0, len(input_configs.sequences), chunk_size)]
    sequences = sequence_chunks[job_idx]

    #import pandas as pd
    #pblms_list = ["homeodomain_PROP1_TGTATT20NGA_TAAT_10_3"]
    #indices = [36144]
    #
    #flank = "".join(["GC"]*13)
    #sequences = []
    #for pblm, idx in list(zip(pblms_list, indices)):
    #    seqs_df = pd.read_csv("/lustre/scratch4/turquoise/akabir/All_dataset_Transformer/selexdata_sequence/"+pblm+".txt", header=None, names=["seq", "binding_value", "not_sure_what"], sep=" ")
    #    seq = seqs_df.loc[idx]["seq"]
    #    out_path = "/lustre/scratch4/turquoise/akabir/outputs_simulation/selex_pydnaepbd_features/"+pblm+"/"
    #    sequences.append((out_path, idx, flank+seq+flank))
    
    #print(sequences)
    print(f"job_idx:{job_idx}, n_seqs:{len(sequences)}")

    run_sequences(sequences, input_configs)
