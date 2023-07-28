import os
import sys

sys.path.append("../pyDNA_EPBD")
home_dir = ""

import numpy as np
import pandas as pd
from models.helpers import (
    get_seqs_encoding,
    compute_and_aggregate_pydna_epbd_features,
    data_format,
)
from sklearn import preprocessing
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm


def do():
    feature_out_dir = f"{ml_outputs_dir}aggregated_features/{seq_filename_wo_ext}/"
    os.makedirs(feature_out_dir, exist_ok=True)

    print("Log: loading features ... ")
    onehot = get_seqs_encoding(df, encoding_type="onehot")
    labels = df["binding_value"].to_numpy()
    coords, flips = compute_and_aggregate_pydna_epbd_features(
        df.shape[0],
        feature_out_dir,
        datatype,
        seq_filename_wo_ext,
        pydna_feature_dir,
        flank_size,
    )
    print(
        f"onehot: {onehot.shape}, coords: {coords.shape}, flips: {flips.shape}, labels: {labels.shape}"
    )

    X, y = np.concatenate([onehot, coords, flips], axis=1), labels
    X = preprocessing.StandardScaler().fit_transform(X)
    y = preprocessing.StandardScaler().fit_transform(y.reshape(-1, 1)).squeeze(1)

    cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)

    regressors = {
        "LR": LinearRegression(),
        "LR_SVR": svm.SVR(kernel="linear"),
        "RBF_SVR": svm.SVR(),
        "DTR": DecisionTreeRegressor(max_depth=10),
        "RFR": RandomForestRegressor(max_depth=10, random_state=0),
    }

    scoring_funcs = ["r2", "neg_mean_squared_error"]

    out_filepath = home_dir + f"{ml_outputs_dir}{seq_filename_wo_ext}.tsv"
    out_file_h = open(out_filepath, "w")

    # out_file_h.write("\t\tOnehot\t\tOnehot+BDs\t\n")
    out_file_h.write(
        f"Data\tMethod\tOnehot R2(avg/std)\tOnehot Negative MSE(avg/std)\tOnehot+BDs R2(avg/std)\tOnehot+BDs Negative MSE(avg/std)\n"
    )
    out_file_h.write(f"{seq_filename_wo_ext}\t")

    for i, (reg_name, reg) in enumerate(regressors.items()):
        print(f"Log: running {reg_name} for {datatype}...")
        onehot_scores = cross_validate(reg, onehot, y, cv=cv, scoring=scoring_funcs)
        onehot_r2_avg, onehot_r2_std = (
            onehot_scores["test_r2"].mean(),
            onehot_scores["test_r2"].std(),
        )
        onehot_neg_mse_avg, onehot_neg_mse_std = (
            onehot_scores["test_neg_mean_squared_error"].mean(),
            onehot_scores["test_neg_mean_squared_error"].std(),
        )

        scores = cross_validate(reg, X, y, cv=cv, scoring=scoring_funcs)
        # print(scores.keys())
        r2_avg, r2_std = scores["test_r2"].mean(), scores["test_r2"].std()
        neg_mse_avg, neg_mse_std = (
            scores["test_neg_mean_squared_error"].mean(),
            scores["test_neg_mean_squared_error"].std(),
        )

        if i != 0:
            out_file_h.write("\t")
        out_file_h.write(
            f"{reg_name}\t{onehot_r2_avg:.3f}/{onehot_r2_std:.3f}\t{onehot_neg_mse_avg:.3f}/{onehot_neg_mse_std:.3f}\t{r2_avg:.3f}/{r2_std:.3f}\t{neg_mse_avg:.3f}/{neg_mse_std:.3f}\n"
        )
        print(
            reg_name,
            f"{onehot_r2_avg:.3f}/{onehot_r2_std:.3f}",
            f"{onehot_neg_mse_avg:.3f}/{onehot_neg_mse_std:.3f}",
            f"{r2_avg:.3f}/{r2_std:.3f}",
            f"{neg_mse_avg:.3f}/{neg_mse_std:.3f}",
            sep="\t",
        )
        # break

    out_file_h.close()


data_root = home_dir + "/usr/projects/pyDNA_EPBD/"
# data_root = home_dir+"data/"
datatype = "selex"

input_seqs_dir = data_root + data_format[datatype]["input_seqs_dir"]
col_names = data_format[datatype]["col_names"]
sep = data_format[datatype]["sep"]
pydna_feature_dir = data_root + data_format[datatype]["pydna_feature_dir"]
flank_size = data_format[datatype]["flank_size"]
ml_outputs_dir = data_root + f"outputs_mls/{datatype}/"
os.makedirs(ml_outputs_dir, exist_ok=True)

job_idx = 0
# array job
if "SLURM_ARRAY_TASK_ID" in os.environ:
    job_idx = int(os.environ["SLURM_ARRAY_TASK_ID"])

seq_files_list = sorted(os.listdir(input_seqs_dir))
seq_filename_with_ext = seq_files_list[job_idx]
# print(seq_files_list)


seq_filename_wo_ext = seq_filename_with_ext[:-4]

df = pd.read_csv(
    input_seqs_dir + seq_filename_with_ext, header=None, names=col_names, sep=sep
)
print(f"{seq_filename_wo_ext}:", df.shape)

do()
print()


