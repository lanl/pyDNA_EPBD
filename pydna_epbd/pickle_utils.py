import pickle
import os


def save_as_pickle(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def create_necessary_directories():
    monitors_output_dirs = [
        "bubble_monitor",
        "coord_monitor",
        "energy_monitor",
        "flipping_monitor",
        "melting_and_fraction_many_monitor",
        "melting_and_fraction_monitor",
        "coord_monitor_verbose",
        "flipping_monitor_verbose",
    ]
    for dir_name in monitors_output_dirs:
        os.makedirs(f"outputs_1/{dir_name}/", exist_ok=True)


def get_dimension(a):
    """given a list (of lists) compute the dimension"""
    if not type(a) == list:
        return []
    return [len(a)] + get_dimension(a[0])


# dim([[1,2,3], [4,5,6]])# [2,3]
