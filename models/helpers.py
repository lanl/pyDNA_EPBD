import os
import sys

sys.path.append("../pyDNA_EPBD")
home_dir = ""

import numpy as np
import pandas as pd

data_format = {
    "selex": {
        "input_seqs_dir": "All_dataset_Transformer/selexdata_sequence/",
        "col_names": ["seq", "binding_value", "not_sure_what"],
        "sep": " ",
        "pydna_feature_dir": "outputs_simulation/selex_pydnaepbd_features/",
        "flank_size": 26,
    },
    "gcpbm": {
        "input_seqs_dir": "All_dataset_Transformer/gcPBMdata_ForRegression/Seqs/",
        "col_names": ["seq", "binding_value"],
        "sep": "\t",
        "pydna_feature_dir": "outputs_simulation/gcpbm_pydnaepbd_features/",
        "flank_size": 4,
    },
}

nucleotides_dict = {"A": 0, "C": 1, "G": 2, "T": 3}


def seq_to_indices(seq: str):
    num_encoded = []
    for ch in seq:
        if ch in nucleotides_dict:
            num_encoded.append(nucleotides_dict[ch])
        else:
            raise Exception(f"'{ch}' is not in 'GCAT'")
    return np.array(num_encoded)


# print(seq_to_indices("ACCT"))


def seq_to_onehot(seq: str):
    one_hot = np.eye(len(nucleotides_dict))[seq_to_indices(seq)]
    return one_hot


# print(seq_to_onehot("ACCT"))


def get_seqs_encoding(df, encoding_type="onehot"):
    # df should have a column with name of "seq", then it will endcode the seqs into onehot or integer
    X = []
    for row in df.itertuples():
        # print(row)
        if encoding_type == "onehot":
            encoded = seq_to_onehot(row.seq)  # onehot
            encoded = np.ravel(encoded)  # flat_onehot
        elif encoding_type == "int":
            encoded = seq_to_indices(row.seq)  # flat_indices
        else:
            raise
        X.append(encoded)
        # if row.Index==10: break
    return np.array(X)


import utils.pickle_utils as pickle_utils


def get_pydna_epbd_feature(
    filename: str, pydna_feature_dir="data/gcpbm_pydnaepbd_features/", flank_size=0
):
    # feature_name:
    #     bubbles (77, 20, 20)
    #     coord (77,)
    #     coord_squared (77,)
    #     flip_verbose (77, 5)

    out_filepath = home_dir + f"{pydna_feature_dir}{filename}.pkl"
    features = pickle_utils.load_pickle(out_filepath)

    coord = features["coord"][flank_size:-flank_size] / 80000  # [4:-4] removing flanks
    flip = (
        features["flip_verbose"][:, 0][flank_size:-flank_size] / 80000
    )  # at 0.707106781186548 Angstrom th
    return coord, flip


def compute_and_aggregate_pydna_epbd_features(
    n_seqs,
    out_dir,
    datatype="gcpbm",
    seq_filename_wo_ext="Mad",
    pydna_feature_dir="data/gcpbm_pydnaepbd_features/",
    flank_size=4,
):
    # out_dir = home_dir+f"models/aggregated_features/{datatype}/{seq_filename_wo_ext}/"
    # os.makedirs(out_dir, exist_ok=True)

    coord_out_path = f"{out_dir}/coords.pkl"
    flip_out_path = f"{out_dir}/flips0.707_allseqs.pkl"
    if os.path.exists(coord_out_path) and os.path.exists(flip_out_path):
        return pickle_utils.load_pickle(coord_out_path), pickle_utils.load_pickle(
            flip_out_path
        )

    # features = np.array([get_pydna_epbd_feature(str(i+1), pydna_feature_dir+seq_filename_wo_ext+"/", flank_size) for i in range(n_seqs)])
    # coords, flips = features[:,0,:], features[:,1,:]

    print(out_dir)
    coords, flips = [], []
    for i in range(n_seqs):
        coord, flip = get_pydna_epbd_feature(
            str(i + 1), pydna_feature_dir + seq_filename_wo_ext + "/", flank_size
        )
        # print(coord.shape, flip.shape)
        coords.append(coord)
        flips.append(flip)
        print(i + 1, coord.shape, flip.shape)
    coords, flips = np.stack(coords, axis=0), np.stack(flips, axis=0)
    # print(coords.shape, flips.shape)
    # raise

    pickle_utils.save_as_pickle(coords, coord_out_path)
    pickle_utils.save_as_pickle(flips, flip_out_path)

    return coords, flips

