from os import sep
from pathlib import Path
import pandas as pd

from adie.nback import read_log, compile_performance, compile_probes

bids_dir = Path("/research/cisc2/projects/critchley_adie/BIDS_data")
sub_probes = []
sub_beh = []
for p in bids_dir.glob("sub-*/**/*task-nback*.tsv"):
    # extract data
    data = read_log(p)
    sub_probes.append(compile_probes(data))
    sub_beh.append(compile_performance(data))

master_probes = pd.concat(sub_probes, axis=0)
master_beh = pd.concat(sub_beh, axis=0)

master_probes.to_csv(bids_dir / "derivatives" / "nback_derivatives" /
    "task-nbackmindwandering_probes.tsv", sep="\t")
master_beh.to_csv(bids_dir / "derivatives" / "nback_derivatives" /
    "task-nbackmindwandering_performance.tsv", sep="\t")