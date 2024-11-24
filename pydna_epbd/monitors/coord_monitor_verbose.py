# this is deprecated, this information is already in the coord-monitor.

# import sys
# sys.path.append("../pyDNA_EPBD")

# import torch

# from monitors.coord_monitor import CoordMonitor
# from simulation.configs import InputConfigs
# from simulation.dna import DNA

# class CoordMonitorVerbose(CoordMonitor):
#     """Average coordinate distance verbose monitor.
#     This generates outputs for every iteration.
#     """
#     def __init__(self, dna:DNA, input_configs:InputConfigs) -> None:
#         super(CoordMonitorVerbose, self).__init__(dna, input_configs)

#     def collect_at_step(self, step_no):
#         return super().collect_at_step(step_no)

#     def output_iter(self):
#         output_file = f"outputs/coord_monitor_verbose/seqidx_{self.seq_idx}_iter_{self.iter_no}.txt"
#         super()._write_file(output_file, self.coord)
