import os
from pydna_epbd.configs import InputConfigs


def read_sequences_from_a_file(input_seqs_dir, filename_with_ext, is_first_col_id, flanks, outputs_dir):
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
            # 1-based increamental id for sequences in a file
            sequences.append((seq_output_dir, seq_id, seq))
    return sequences


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
        seqs = read_sequences_from_a_file(input_seqs_dir, filename_with_ext, is_first_col_id, flanks, outputs_dir)
        all_seqs += seqs

        n_bps = len(seqs[0][2]) - (2 * len(flanks))
        total_num_of_bps += len(seqs) * n_bps
        # print(filename_with_ext, len(seqs), n_bps, total_num_of_bps)
        # if i==2: break

    print(f"total #-seqs: {len(all_seqs)}")
    print(f"total #-bps (w/o flanks): {total_num_of_bps}")
    # print(all_seqs[:3])
    return all_seqs


def read_configurations(configuration_filepath):
    """Read the configs from the input configuration file.

    Args:
        configuration_filepath (str): The configurations needed to run MCMC simulations.
            The structure of the configs are given in the Readme file.

    Returns:
        InputConfigs: The class containing specific format for running the simulations.
    """

    # parsing configuration file
    configs = {}
    with open(configuration_filepath, "r") as myfile:
        for line in myfile:
            name, val = line.partition("=")[::2]
            configs[name.strip()] = val.strip()

    # global simulation configs
    is_first_col_id = configs["IsFirstColumnId"] == "Yes"
    save_full = configs["SaveFull"] == "Yes"
    save_runtime = configs["SaveRuntime"] == "Yes"
    input_seqs_dir = configs["SequencesDir"]
    outputs_dir = configs["OutputsDir"]
    flanks = "" if configs["Flanks"] == "None" else configs["Flanks"]
    temperature = float(configs["Temperature"])
    n_iterations = int(configs["Iterations"])
    n_preheating_steps = int(configs["PreheatingSteps"])
    n_post_preheating_steps = int(configs["PostPreheatingSteps"])
    n_nodes = int(configs["ComputingNodes"])

    # monitor configs
    os.environ["BUBBLE_MONITOR"] = configs["BubbleMonitor"]
    os.environ["COORD_MONITOR"] = configs["CoordinateMonitor"]
    os.environ["FLIPPING_MONITOR_VERBOSE"] = configs["FlippingMonitorVerbose"]
    os.environ["FLIPPING_MONITOR"] = configs["FlippingMonitor"]
    os.environ["ENERGY_MONITOR"] = configs["EnergyMonitor"]
    os.environ["MELTING_AND_FRACTION_MONITOR"] = configs["MeltingAndFractionMonitor"]
    os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] = configs["MeltingAndFractionManyMonitor"]

    # reading sequences and creating outputs directory
    sequences = read_all_sequences(input_seqs_dir, is_first_col_id, flanks, outputs_dir)

    input_configs = InputConfigs(
        temperature,
        sequences,
        outputs_dir,
        n_iterations,
        n_preheating_steps,
        n_post_preheating_steps,
        n_nodes,
        save_full,
        save_runtime,
    )

    print(input_configs)
    return input_configs


# read_configurations("../examples/configs.txt")
