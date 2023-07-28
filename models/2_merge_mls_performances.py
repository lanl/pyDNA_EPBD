import os
import sys

sys.path.append("../pyDNA_EPBD")
home_dir = ""

import pandas as pd

datatype = "selex"  # gcpbm, selex
data_root = home_dir + "/usr/projects/pyDNA_EPBD/"
# data_root = home_dir+"data/"
ml_outputs_dir = data_root + f"outputs_mls/{datatype}/"
out_files_list = sorted(os.listdir(ml_outputs_dir))

dfs = []
n_files = 1
for out_file in out_files_list:
    if not out_file.endswith(".tsv"):
        continue
    print(n_files, out_file)
    df = pd.read_csv(f"{ml_outputs_dir}{out_file}", sep="\t")
    dfs.append(df)
    n_files += 1

merged_df = pd.concat(dfs)
merged_df.to_csv(
    f"{data_root}outputs_mls/aggregated_performance_{datatype}.tsv",
    index=False,
    sep="\t",
)
