from adie.nback import read_log, extract_stimtype

from pathlib import Path
import pandas as pd


data, filename = read_log(Path("test/data/sub-999_ses-baseline_task-nbackmindwandering_beh.tsv"))
columns = ["StimIndex", 'nBack', 'fixStart', 'stimStart', 'mwType', 'keyResp', 'respRT']
sliced = extract_stimtype(data, filename, "MWQ", columns)

# extract data
# disgusting one liner to get all thought probes
probes = pd.concat([entry.loc[:, ["keyResp"]].reset_index(drop=True).rename({"keyResp": item}, axis=1)
    for item, entry in sliced.groupby("mwType")], axis=1)
nback = sliced.query("mwType == 'Focus'")[
  ["participant_id", "ses","nBack"]].reset_index(drop=True)
idx_start = sliced.query("mwType == 'Focus'").index
idx_end = idx_start + 12
probe_start = sliced.loc[idx_start, "stimStart"].reset_index(drop=True)
prob_end = sliced.loc[idx_end, ["stimStart", "respRT"]].reset_index(drop=True).sum(axis=1)
prob_end.name = "stimEnd"
probes = pd.concat([nback, probe_start, prob_end, probes], axis=1)
probes.index.name = "probe_index"