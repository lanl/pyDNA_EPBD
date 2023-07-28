import os
import sys
sys.path.append("../pyDNA_EPBD")
home_dir=""

from simulation.configs import InputConfigs

def read_sequences_from_a_file(input_seqs_dir, filename_with_ext):
    sequences = []
    flank = "GCGC"
    filepath = input_seqs_dir+filename_with_ext
    filename_wo_ext = filename_with_ext[:-4]

    with open(filepath, "r") as f:
        for i, line in enumerate(f.readlines()):
            line_items = line.split()
            seq = line_items[0].strip()
            seq = flank+seq+flank
            sequences.append((filename_wo_ext, i+1, seq)) # 1-based increamental id for sequences in a file

    return sequences


def read_all_sequences(input_seqs_dir):
    all_seqs = []
    for i, filename_with_ext in enumerate(os.listdir(input_seqs_dir)):
        seqs = read_sequences_from_a_file(input_seqs_dir, filename_with_ext)
        all_seqs += seqs
        # print(filename_with_ext, f"#-seqs: {len(seqs)}")
        # if i==2: break

    # print(f"total #-seqs: {len(all_seqs)}")
    # print(all_seqs[:3])
    return all_seqs


def read_input_data(configuration_filepath):
    with open(configuration_filepath, "r") as file:
        ret = file.readline().strip().split()
        sequences = read_all_sequences(ret[1]) # Reading sequences containing directory

        ret = file.readline().strip().split()
        outputs_dir = ret[1]

        ret = file.readline().strip().split()
        temperature = float(ret[1])

        ret = file.readline().strip().split()
        n_iterations = int(ret[1]) # Reading the number of iterations

        ret = file.readline().strip().split()
        n_preheating_steps = int(ret[1]) # Reading the number of Preheating

        ret = file.readline().strip().split()
        n_steps_after_preheating = int(ret[1]) # Reading the number of after preheating steps

        ret = file.readline().strip().split()
        n_nodes = int(ret[1])

        ret = file.readline().strip().split()
        n_jobs = int(ret[1])


    input_configs = InputConfigs(temperature, sequences, outputs_dir, n_iterations, n_preheating_steps, n_steps_after_preheating, n_nodes, n_jobs)
    print(input_configs)
    return input_configs

# read_input_data("gcpbm/configs/hopper.txt")