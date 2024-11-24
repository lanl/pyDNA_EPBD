import os, time
from pydna_epbd.simulation.dna import DNA
from pydna_epbd.simulation.mc_simulation import Simulation
from pydna_epbd.monitors.all_monitors import Monitors
from pydna_epbd.simulation.aggregate_outputs_and_write import aggregate_outputs_for_single_temp
from joblib import delayed, Parallel
import pydna_epbd.pickle_utils as utils


def run_single_iteration(n_preheating_steps, n_steps_after_preheating, seq_id, seq, temp, iter_no):
    """This runs a single MCMC simulation iteration.

    Args:
        n_preheating_steps (int): Number of preheating steps (from input config).
        n_steps_after_preheating (int): Number of post preheating steps (from input config).
        seq_id (str): Seq-id attached to each input sequence.
        seq (str): DNA sequence.
        temp (float): Temperature in Kelvin (from input config).
        iter_no (int): Iteration index.

    Returns:
        Monitors: A Monitors object.
    """
    # every iteration is independent
    # start_time = time.time()
    total_steps = n_preheating_steps + n_steps_after_preheating

    dna = DNA(seq)

    monitors = Monitors(dna, n_preheating_steps, n_steps_after_preheating)
    monitors.update_state(seq_id, temp, iter_no)

    simulation = Simulation(dna)
    simulation.init_temp(temp)

    simulation.execute(monitors, total_steps, n_preheating_steps)
    monitors.collect_at_iter()
    # print(f"finished -> seq_id:{seq_id} | temp:{temp} | iter:{iter_no} -> {(time.time()-start_time)} seconds to execute") # per iteration time log

    return monitors


def run_sequences(sequences, input_configs):
    """Main function to run MCMC simulations for all DNA sequences. This initializes 100 or the number of available cpu cores-1 cpus
    to parallaly run n_iterations.

    Args:
        sequences (list): List of tuples. Format: [("seq_output_dir", "seq_id", "seq")]
        input_configs (InputConfigs): A InputConfigs object contaning all configurations.
    """
    if input_configs.save_runtime:
        runtime_filepath = "runtimes/" + sequences[0][0].split("/")[-2] + ".txt"
        # print(runtime_filepath)
        runtime_write_mode = "a" if os.path.exists(runtime_filepath) else "w"
        runtime_out_handle = open(runtime_filepath, runtime_write_mode)

    with Parallel(n_jobs=os.cpu_count() - 3, verbose=1) as parallel:  # min(100, os.cpu_count() - 1)
        for i in range(0, len(sequences)):
            seq_output_dir, seq_id, seq = sequences[i]
            simulation_out_filepath = f"{seq_output_dir}{seq_id}.pkl"

            # checking whether the simulation is run previously for this seq_id and output is correct
            if os.path.exists(simulation_out_filepath):
                try:
                    x = utils.load_pickle(simulation_out_filepath)
                    print("Already computed:", simulation_out_filepath)
                    continue
                except Exception as e:
                    print(f"Previously computed '{simulation_out_filepath}' had issues, computing again ... ")
                    # raise e
            # else:
            k = 0
            # for k in range(10): # for 10 runs to do runtime analysis

            print(f"Running simulation: seq_idx:{i} | seq_id:{seq_id}")
            start_time = time.time()

            list_of_monitors = parallel(
                delayed(run_single_iteration)(
                    input_configs.n_preheating_steps, input_configs.n_steps_after_preheating, seq_id, seq, input_configs.temperature, iter_no
                )
                for iter_no in range(input_configs.n_iterations)
            )

            assert (
                len(list_of_monitors) == input_configs.n_iterations
            ), f"Should be equal, but found {len(list_of_monitors)} != {input_configs.n_iterations}"  # synchronization barrier

            aggregate_outputs_for_single_temp(list_of_monitors, input_configs, simulation_out_filepath)

            runtime = time.time() - start_time
            print(f"finished -> {simulation_out_filepath} -> {runtime} seconds to execute")
            if input_configs.save_runtime:
                runtime_out_handle.write(f"{k}:{simulation_out_filepath}:{runtime}\n")

            # break # to run 1st seq, comment-out this line
    if input_configs.save_runtime:
        runtime_out_handle.close()


# temp_idx = 0
# for seq_idx in range(0, len(sequences)):
#     seq_name, seq = sequences[seq_idx]
#     if os.path.exists(f"{input_configs.outputs_dir}{seq_name}.pkl"):
#         print("Already computed:", f"{input_configs.outputs_dir}{seq_name}.pkl")
#     else:
#         print(f"Running simulation for seq_idx:{seq_idx} | seq_name:{seq_name}")
#         # run_single_sequence(seq_name, seq)
#         list_of_monitors = run_single_temp(seq_name, seq, temp_idx)
#         aggregate_outputs_for_single_temp(seq_name, seq, list_of_monitors, input_configs)

#     if seq_idx==1: break # to run 1st seq, comment-out this line

# def collect_at_temp(monitors:Monitors):
#     monitors.collect_at_temp()
#     return monitors

# def run_single_temp(seq_name, seq, temp_idx):
#     list_of_monitors = Parallel(n_jobs=47, verbose=1)(delayed(run_single_iter)(seq_name, seq, temp_idx, iter_no) for iter_no in range(input_configs.n_iterations))
#     # list_of_monitors = Parallel(n_jobs=47, verbose=1)(delayed(collect_at_temp)(monitors) for monitors in list_of_monitors)
#     return list_of_monitors # corresponding to n-iterations of the same temp

# def run_single_sequence(seq_name, seq):
#     # corrsponding to n-temps n-iters of the same seq
#     list_of_list_of_monitors = Parallel(n_jobs=input_configs.n_temperatures, verbose=1)(delayed(run_single_temp)(seq_name, seq, temp_idx) for temp_idx in range(input_configs.n_temperatures))
#     aggregate_outputs_for_many_temp(seq_name, seq, list_of_list_of_monitors, input_configs) # aggregating all iterations for a 'seq' at 'temp'
