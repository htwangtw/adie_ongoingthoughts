from os import sep
from pathlib import Path

import json

import pandas as pd

from adie.nback import (
    read_log,
    compile_performance,
    compile_probes,
    compile_ses,
)

bids_dir = Path("__file__").parent  # this file is in BIDS_data/code
sub_probes = []
sub_beh = []
sub_ses = []
for p in bids_dir.glob("sub-*/**/*task-nback*.tsv"):
    # extract data
    data = read_log(p)
    sub_probes.append(compile_probes(data))
    sub_beh.append(compile_performance(data))
    sub_ses.append(compile_ses(data))

master_probes = pd.concat(sub_probes, axis=0)
master_beh = pd.concat(sub_beh, axis=0)
master_ses = pd.concat(sub_ses, axis=0)

master_probes.to_csv(
    bids_dir
    / "derivatives"
    / "nback_derivatives"
    / "task-nbackmindwandering_probes.tsv",
    sep="\t",
)
master_beh.to_csv(
    bids_dir
    / "derivatives"
    / "nback_derivatives"
    / "task-nbackmindwandering_performance.tsv",
    sep="\t",
    index=False,
)
master_ses.to_csv(
    bids_dir
    / "derivatives"
    / "nback_derivatives"
    / "task-nbackmindwandering_sessionthough.tsv",
    sep="\t",
)


# get the full question of thought probe
probe_json = bids_dir / "derivatives" / "nback_derivatives" / "probes.json"
session_json = (
    bids_dir / "derivatives" / "nback_derivatives" / "sessionend.json"
)
if not probe_json.is_file:
    es_probe = data.query('stimType == "MWQ"')

    es_probe = es_probe.reset_index().loc[:13, ["mwType", "stimPic", "Ans"]]

    probes = {}
    for a, full in es_probe.set_index(["mwType"]).iterrows():
        probes[a] = {"question": full["stimPic"], "scale": full["Ans"]}

    with open(probe_json) as f:
        json.dump(probes, f, indent=2)

if not session_json.is_file:
    es_end = es_end.reset_index().loc[:, ["mwType", "stimPic", "Ans"]]

    end = {}
    for a, full in es_end.set_index(["mwType"]).iterrows():
        end[a] = {"question": full["stimPic"], "scale": full["Ans"]}
    with open(session_json) as f:
        json.dump(end, f, indent=2)
