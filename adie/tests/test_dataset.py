from pathlib import Path
import io
import numpy as np

from adie.dataset import *
from adie.tests import get_test_data_path

bids_dir = Path(get_test_data_path()) / "adie_data"
test_file = Path(get_test_data_path()) / "file.smr"

signal_info = [
    {
        "SamplingFrequency": 100,
        "StartTime": 0.0,
        "Columns": ["ecg"],
        "ecg": {"Unit": "unknown"},
    },
    {
        "SamplingFrequency": 100,
        "StartTime": 0.0,
        "Columns": ["stim"],
        "stim": {"Unit": "unknown"},
    },
]
signals = [np.array([34, 45, 23]), np.array([34, 45, 23])]


def test_pasreinfo():
    sub, ses, group = parseinfo("CONADIE983")
    assert sub == "CONADIE983"
    assert group == "control"
    assert ses == "baseline"

    sub, ses, group = parseinfo("ADIE983_FY")
    assert sub == "ADIE983"
    assert group == "patient"
    assert ses == "oneyear"

    sub, ses, group = parseinfo("ADIE983F")
    assert sub == "ADIE983"
    assert group == "patient"
    assert ses == "oneweek"

    sub, ses, group = parseinfo("ADIE983_BL")
    assert sub == "ADIE983"
    assert group == "patient"
    assert ses == "baseline"


def test_gen_bidsbeh(tmpdir):
    print("check template")
    path, bn = gen_bidsbeh(str(tmpdir), "ADIE983", session="baseline")
    assert path == Path(tmpdir) / "sub-ADIE983/ses-baseline/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983_ses-baseline"

    print("single session")
    path, bn = gen_bidsbeh(tmpdir, "ADIE983")
    assert path == tmpdir / "sub-ADIE983/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983"

    print("check file creation")
    path, bn = gen_bidsbeh(tmpdir, "ADIE983", "baseline")
    assert bn == "sub-ADIE983_ses-baseline"
    assert path == tmpdir / "sub-ADIE983/ses-baseline/beh"

    print("derivative, no session")
    path, bn = gen_bidsbeh(tmpdir, "ADIE983", derivative="mytask")
    assert path == Path(tmpdir) / "derivatives/mytask/sub-ADIE983/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983"


def test_conver_beh(tmpdir):
    origin = bids_dir / "sourcedata/ADIE983_beh_task.csv"
    saved_loc = convert_beh(
        origin, tmpdir, "sub-ADIE983_ses-baseline", "mytask"
    )
    assert saved_loc == tmpdir / "sub-ADIE983_ses-baseline_task-mytask_beh.tsv"

    # run again, the file should exist already, hence pass coverage
    saved_loc = convert_beh(
        origin, tmpdir, "sub-ADIE983_ses-baseline", "mytask"
    )
    assert saved_loc == tmpdir / "sub-ADIE983_ses-baseline_task-mytask_beh.tsv"


def test_name_physiobids():
    names = name_physiobids("sub-ADIE983_ses-baseline", "mytask", signal_info)
    assert len(names) == len(signal_info)
    assert (
        names[0] == "sub-ADIE983_ses-baseline_task-mytask_recording-ecg_physio"
    )
    assert names[1] == "sub-ADIE983_ses-baseline_task-mytask_stim"


def test_save_physio(tmpdir):
    bidsnames = name_physiobids(
        "sub-ADIE983_ses-baseline", "mytask", signal_info
    )
    saved = save_physio(
        tmpdir, "sub-ADIE983_ses-baseline", "mytask", test_file
    )
    assert len(saved) == len(bidsnames)
    assert saved[0] == str(tmpdir / bidsnames[0])
    assert saved[1] == str(tmpdir / bidsnames[1])


def test_smr_derivative(tmpdir):
    sub_path, bn = gen_bidsbeh(tmpdir, "ADIE983", derivative="physio_smr")
    saved = smr_derivative(
        test_file, tmpdir, "ADIE983", "mytask", recording="ecg"
    )
    assert saved == sub_path / f"{bn}_task-mytask_recording-ecg_physio.smr"
    assert saved.is_file() is True
