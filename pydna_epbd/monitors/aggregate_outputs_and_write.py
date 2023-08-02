import os
import pydna_epbd.utils.pickle_utils as utils
import numpy as np


def aggregate_outputs_for_single_temp(list_of_monitors, input_configs, out_filepath):
    """Collect outputs of all the monitors from independent iterations and save them as dictionary object.
    An example output pickle file looks like the following when only the bubble and coordinate monitors are switched on:
    {"bubbles": numpy.ndarray, "coord": numpy.ndarray}

    Args:
        list_of_monitors (list): List of monitors.
        input_configs (InputConfigs): An InputConfigs object.
        out_filepath (str): Directory path to save the simulation output.
    """
    bubble_iter_list, coord_iter_list, coord_squared_iter_list, energy_iter_list = (
        [],
        [],
        [],
        [],
    )
    flip_iter_list, flip_verbose_iter_list = [], []
    melting_iter_list, fraction_iter_list = [], []
    melting_many_iter_list, fraction_many_iter_list = [], []

    for iter_no in range(input_configs.n_iterations):
        monitors = list_of_monitors[iter_no]
        if os.environ["BUBBLE_MONITOR"] == "True":
            bubble_iter_list.append(monitors.bubble_monitor.bubbles)

        if os.environ["COORD_MONITOR"] == "True":
            coord_iter_list.append(monitors.coord_monitor.coord)
            coord_squared_iter_list.append(monitors.coord_monitor.coord_square)

        if os.environ["FLIPPING_MONITOR"] == "True":
            flip_iter_list.append(monitors.flipping_monitor.flip)

        if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
            flip_verbose_iter_list.append(monitors.flipping_monitor_verbose.flip)

        if os.environ["ENERGY_MONITOR"] == "True":
            energy_iter_list.append(monitors.energy_monitor.energy)

        if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
            melting_iter_list.append(monitors.melting_and_fraction_monitor.melting)
            fraction_iter_list.append(monitors.melting_and_fraction_monitor.fraction)

        if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
            melting_many_iter_list.append(
                monitors.melting_and_fraction_many_monitor.melting_many
            )
            fraction_many_iter_list.append(
                monitors.melting_and_fraction_many_monitor.fraction_many
            )

    # formating outputs as dictionary, all features are averaged over the number of iterations
    outputs = {}
    if os.environ["BUBBLE_MONITOR"] == "True":
        # (n_iters, seq_len, max_bubble_elem=20, thr_sizes=20)
        outputs["bubbles"] = (
            np.array(bubble_iter_list)
            if input_configs.save_full
            else np.array(bubble_iter_list).mean(0)
        )

    if os.environ["COORD_MONITOR"] == "True":
        # (n_iters, seq_len)
        outputs["coord"] = (
            np.array(coord_iter_list)
            if input_configs.save_full
            else np.array(coord_iter_list).mean(0)
        )

        # (n_iters, seq_len)
        outputs["coord_squared"] = (
            np.array(coord_squared_iter_list)
            if input_configs.save_full
            else np.array(coord_squared_iter_list).mean(0)
        )

    if os.environ["FLIPPING_MONITOR"] == "True":
        # (n_iters, seq_len)
        outputs["flip"] = (
            np.array(flip_iter_list).mean(0)
            if input_configs.save_full
            else np.array(flip_iter_list).mean(0)
        )

    if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
        # (n_iters, seq_len, flip_sizes=10)
        outputs["flip_verbose"] = (
            np.array(flip_verbose_iter_list)
            if input_configs.save_full
            else np.array(flip_verbose_iter_list).mean(0)
        )

    if os.environ["ENERGY_MONITOR"] == "True":
        # (n_iters, total_steps)
        outputs["energy"] = (
            np.array(energy_iter_list)
            if input_configs.save_full
            else np.array(energy_iter_list).mean(0)
        )

    if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
        # (n_iters)
        outputs["melting"] = (
            np.array(melting_iter_list)
            if input_configs.save_full
            else np.array(melting_iter_list).mean(0)
        )

        # (n_iters)
        outputs["fraction"] = (
            np.array(fraction_iter_list)
            if input_configs.save_full
            else np.array(fraction_iter_list).mean(0)
        )

    if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
        # (n_iters, n_time_steps=100, melt_faction_sizes=20)
        outputs["melting_many"] = (
            np.array(melting_many_iter_list)
            if input_configs.save_full
            else np.array(melting_many_iter_list).mean(0)
        )

        # (n_iters, n_time_steps=100, melt_faction_sizes=20)
        outputs["fraction_many"] = (
            np.array(fraction_many_iter_list)
            if input_configs.save_full
            else np.array(fraction_many_iter_list).mean(0)
        )

    utils.save_as_pickle(outputs, out_filepath)

    for key, _ in outputs.items():
        if input_configs.save_full:
            print("\t", key, outputs[key].shape)
        else:
            print("\t", key, outputs[key].shape)  # utils.get_dimension(outputs[key]))


# this function is outdated.
# def aggregate_outputs_for_many_temp(
#     seq_name, seq, list_of_list_of_monitors, input_configs
# ):
#     """list_of_list_of_monitors: List[List[Monitors]]
#     input_configs:InputConfigs
#     """
#     # seq_name, seq = input_configs.sequences[seq_idx]

#     # aggregating all iterations for a 'seq' at 'temp'
#     bubble_list, coord_list, coord_square_list, energy_list = [], [], [], []
#     flip_list, flip_verbose_list = [], []
#     melting_list, fraction_list = [], []
#     melting_many_list, fraction_many_list = [], []

#     for temp_idx in range(input_configs.n_temperatures):
#         bubble_iter_list, coord_iter_list, coord_square_iter_list, energy_iter_list = (
#             [],
#             [],
#             [],
#             [],
#         )
#         flip_iter_list, flip_verbose_iter_list = [], []
#         melting_iter_list, fraction_iter_list = [], []
#         melting_many_iter_list, fraction_many_iter_list = [], []

#         for iter_no in range(input_configs.n_iterations):
#             monitors = list_of_list_of_monitors[temp_idx][iter_no]
#             if os.environ["BUBBLE_MONITOR"] == "True":
#                 bubble_iter_list.append(monitors.bubble_monitor.bubbles)

#             if os.environ["COORD_MONITOR"] == "True":
#                 coord_iter_list.append(monitors.coord_monitor.coord)
#                 coord_square_iter_list.append(monitors.coord_monitor.coord_square)

#             if os.environ["FLIPPING_MONITOR"] == "True":
#                 flip_iter_list.append(monitors.flipping_monitor.flip)

#             if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
#                 flip_verbose_iter_list.append(monitors.flipping_monitor_verbose.flip)

#             if os.environ["ENERGY_MONITOR"] == "True":
#                 energy_iter_list.append(monitors.energy_monitor.energy)

#             if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
#                 melting_iter_list.append(monitors.melting_and_fraction_monitor.melting)
#                 fraction_iter_list.append(
#                     monitors.melting_and_fraction_monitor.fraction
#                 )

#             if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
#                 melting_many_iter_list.append(
#                     monitors.melting_and_fraction_many_monitor.melting_many
#                 )
#                 fraction_many_iter_list.append(
#                     monitors.melting_and_fraction_many_monitor.fraction_many
#                 )

#         if os.environ["BUBBLE_MONITOR"] == "True":
#             bubble_list.append(bubble_iter_list)
#         if os.environ["COORD_MONITOR"] == "True":
#             coord_list.append(coord_iter_list)
#             coord_square_list.append(coord_square_iter_list)
#         if os.environ["FLIPPING_MONITOR"] == "True":
#             flip_list.append(flip_iter_list)
#         if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
#             flip_verbose_list.append(flip_verbose_iter_list)
#         if os.environ["ENERGY_MONITOR"] == "True":
#             energy_list.append(energy_iter_list)
#         if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
#             melting_list.append(melting_iter_list)
#             fraction_list.append(fraction_iter_list)
#         if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
#             melting_many_list.append(melting_many_iter_list)
#             fraction_many_list.append(fraction_many_iter_list)

#     # formating outputs as dictionary
#     outputs = {}
#     if os.environ["BUBBLE_MONITOR"] == "True":
#         outputs[
#             "bubbles"
#         ] = bubble_list  # (n_temps, n_iters, seq_len, max_bubble_elem=20, thr_sizes=20)
#     if os.environ["COORD_MONITOR"] == "True":
#         outputs["coord"] = coord_list  # (n_temps, n_iters, seq_len)
#         outputs["coord_square"] = coord_square_list  # (n_temps, n_iters, seq_len)
#     if os.environ["FLIPPING_MONITOR"] == "True":
#         outputs["flip"] = flip_list  # (n_temps, n_iters, seq_len)
#     if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
#         outputs[
#             "flip_verbose"
#         ] = flip_verbose_list  # (n_temps, n_iters, seq_len, flip_sizes=10)
#     if os.environ["ENERGY_MONITOR"] == "True":
#         outputs["energy"] = energy_list  # (n_temps, n_iters, total_steps)
#     if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
#         outputs["melting"] = melting_list  # (n_temps, n_iters)
#         outputs["fraction"] = fraction_list  # (n_temps, n_iters)
#     if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
#         outputs[
#             "melting_many"
#         ] = melting_many_list  # (n_temps, n_iters, n_time_steps=100, melt_faction_sizes=20)
#         outputs[
#             "fraction_many"
#         ] = fraction_many_list  # (n_temps, n_iters, n_time_steps=100, melt_faction_sizes=20)

#     out_dir = (
#         input_configs.outputs_dir
#     )  # f"/lustre/scratch4/turquoise/akabir/outputs_simulation_large/"
#     out_filepath = f"{out_dir}{seq_name}.pkl"
#     utils.save_as_pickle(outputs, out_filepath)

#     # outputs = utils.load_pickle(out_filepath)
#     print(f"\t---{seq_name}---")
#     for key, _ in outputs.items():
#         print("\t", key, utils.get_dimension(outputs[key]))
