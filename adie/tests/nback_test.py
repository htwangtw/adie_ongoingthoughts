from pathlib import Path
import pandas as pd

import pytest

from adie.nback import read_log, extract_stimtype
from adie.tests import get_test_data_path


testdata = Path(get_test_data_path()) / "sub-999_ses-baseline_task-nbackmindwandering_beh.tsv"

def test_read_log():
    data = read_log(testdata)
    filename, data = data.popitem()
    assert filename == "sub-999_ses-baseline_task-nbackmindwandering_beh.tsv"

def test_extract_stimtype():
    data = read_log(testdata)
    filename, data = data.popitem()
    columns = ["StimIndex", 'nBack', 'fixStart', 'stimStart', 'mwType', 'keyResp', 'respRT']

    with pytest.raises(ValueError, ):
        extract_stimtype(data, filename, "blah", columns)

    sliced = extract_stimtype(data, filename, "MWQ", columns)
    assert sliced.shape[1] == len(columns) + 2  # subject id and sesstion



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