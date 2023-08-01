import os

home_dir = ""

from configs.input_configs import InputConfigs


def read_sequences_from_a_file(
    input_seqs_dir, filename_with_ext, is_first_col_id, flanks, outputs_dir
):
    """Read DNA sequences from one input file. This also creates output directories for saving simulation outputs.

    Args:
        input_seqs_dir (str): Directory that contains DNA sequences file.
        filename_with_ext (str): Filename with extension.
        is_first_col_id (bool): Whether or not the first column of the sequence containing file determines sequence id.
        flanks (str): Flanks are added at both sides of all input sequences.
        outputs_dir (str): The output directory for saving simulation outputs.

    Returns:
        list: A list of tuples containing all sequences in the input sequence file with seq-id and output directory.
        If seq-id is not present, 1-indexed incrementally generated seq-id will be attached.
        Format: [("seq_output_dir", "seq_id", "seq")]
    """
    sequences = []
    # flanks = ""#.join(["GC"]*13) # 26 GCs on both sides
    filepath = input_seqs_dir + filename_with_ext
    filename_wo_ext = filename_with_ext[:-4]

    seq_output_dir = f"{outputs_dir}{filename_wo_ext}/"
    os.makedirs(seq_output_dir, exist_ok=True)

    with open(filepath, "r") as f:
        for i, line in enumerate(f.readlines()):
            line_items = line.split()
            if is_first_col_id:
                seq_id, seq = line_items[0].strip(), line_items[1].strip()
            else:
                seq_id, seq = i + 1, line_items[0].strip()

            seq = flanks + seq + flanks
            sequences.append(
                (seq_output_dir, seq_id, seq)
            )  # 1-based increamental id for sequences in a file
    return sequences


# print(read_sequences_from_a_file.__doc__)


def read_all_sequences(input_seqs_dir, is_first_col_id, flanks, outputs_dir):
    """Read all sequences for the simulation.

    Args:
        input_seqs_dir (str): Directory that contains files containing DNA sequences.
        is_first_col_id (bool): Whether or not the first column of the sequence containing file determines sequence id.
        flanks (str): Flanks are added at both sides of all input sequences.
        outputs_dir (str): The output directory for saving simulation outputs.

    Returns:
        list: A list containing all sequences in the input directory.
    """
    all_seqs = []
    total_num_of_bps = 0
    for i, filename_with_ext in enumerate(os.listdir(input_seqs_dir)):
        seqs = read_sequences_from_a_file(
            input_seqs_dir, filename_with_ext, is_first_col_id, flanks, outputs_dir
        )
        all_seqs += seqs

        n_bps = len(seqs[0][2]) - (2 * len(flanks))
        total_num_of_bps += len(seqs) * n_bps
        # print(filename_with_ext, len(seqs), n_bps, total_num_of_bps)
        # if i==2: break

    print(f"total #-seqs: {len(all_seqs)}")
    print(f"total #-bps (w/o flanks): {total_num_of_bps}")
    # print(all_seqs[:3])
    return all_seqs


def read_input_data(configuration_filepath):
    """Read the configs from the input configuration file.

    Args:
        configuration_filepath (str): The configurations needed to run MCMC simulations.
            The structure of the configs are given in the Readme file.

    Returns:
        InputConfigs: The class containing specific format for running the simulations.
    """
    with open(configuration_filepath, "r") as file:
        ret = file.readline().strip().split()
        is_first_col_id = ret[1] == "Yes"

        ret = file.readline().strip().split()
        input_seqs_dir = ret[1]

        ret = file.readline().strip().split()
        outputs_dir = ret[1]

        ret = file.readline().strip().split()
        save_full = ret[1] == "Yes"

        ret = file.readline().strip().split()
        save_runtime = ret[1] == "Yes"

        ret = file.readline().strip().split()
        flanks = "" if ret[1] == "None" else ret[1]

        sequences = read_all_sequences(
            input_seqs_dir, is_first_col_id, flanks, outputs_dir
        )

        ret = file.readline().strip().split()
        temperature = float(ret[1])

        ret = file.readline().strip().split()
        n_iterations = int(ret[1])  # Reading the number of iterations

        ret = file.readline().strip().split()
        n_preheating_steps = int(ret[1])  # Reading the number of Preheating

        ret = file.readline().strip().split()
        n_steps_after_preheating = int(
            ret[1]
        )  # Reading the number of after preheating steps

        ret = file.readline().strip().split()
        n_nodes = int(ret[1])

    input_configs = InputConfigs(
        temperature,
        sequences,
        outputs_dir,
        n_iterations,
        n_preheating_steps,
        n_steps_after_preheating,
        n_nodes,
        save_full,
        save_runtime,
    )
    print(input_configs)
    return input_configs
