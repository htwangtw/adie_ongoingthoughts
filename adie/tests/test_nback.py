from pathlib import Path
import pandas as pd

import pytest

from adie.nback import read_log, extract_stimtype, compile_probes, compile_performance, compile_ses
from adie.tests import get_test_data_path


testdata = Path(get_test_data_path()) / "sub-999_ses-baseline_task-nbackmindwandering_beh.tsv"
mwq = ["StimIndex", 'nBack', 'fixStart', 'stimStart', 'mwType', 'keyResp', 'respRT']

def test_nback():
    data = read_log(testdata)
    assert "participant_id" in data.columns
    assert "ses" in data.columns
    assert "run" not in data.columns

    with pytest.raises(ValueError):
        extract_stimtype(data, "blah", mwq)

    sliced = extract_stimtype(data, "MWQ", mwq)
    assert len(mwq) == 7  # original input ketp un changed
    assert sliced.shape[1] == 9 # subject id and sesstion

    probes = compile_probes(data)
    assert probes.shape[0] == 12
    assert probes.shape[1] == 18

    beh = compile_performance(data)
    assert beh.shape[0] == 3

    ses = compile_ses(data)
    assert ses.shape[0] == 1