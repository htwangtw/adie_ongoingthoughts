from adie.dataset import *

from pathlib import Path
import io
import numpy as np


bidsroot = Path(__file__).parent / "data/bids_test"
signal_info = [{"SamplingFrequency": 100,
                "StartTime": 0.0,
                "Columns": ["ecg"],
                "ecg": {"Unit": "unknown"}
                },
                {"SamplingFrequency": 100,
                "StartTime": 0.0,
                "Columns": ["stim"],
                "stim": {"Unit": "unknown"}}
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
    assert ses == "1yf"

    sub, ses, group = parseinfo("ADIE983F")
    assert sub == "ADIE983"
    assert group == "patient"
    assert ses == "3mf"

    sub, ses, group = parseinfo("ADIE983_BL")
    assert sub == "ADIE983"
    assert group == "patient"
    assert ses == "baseline"

def test_gen_bidsbeh(tmpdir):
    print("check template")
    path, bn = gen_bidsbeh(bidsroot, "ADIE983", session="baseline")
    assert path == Path(bidsroot) / "sub-ADIE983/ses-baseline/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983_ses-baseline"

    print("single session")
    path, bn = gen_bidsbeh(bidsroot, "ADIE983")
    assert path == Path(bidsroot) / "sub-ADIE983/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983"

    print("check file creation")
    path, bn = gen_bidsbeh(tmpdir, "ADIE983", "baseline")
    assert bn == "sub-ADIE983_ses-baseline"
    assert path == tmpdir / "sub-ADIE983/ses-baseline/beh"

    print("derivative, no session")
    path, bn = gen_bidsbeh(bidsroot, "ADIE983", derivative="mytask")
    assert path == Path(bidsroot) / "derivatives/mytask/sub-ADIE983/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983"

def test_conver_beh(tmpdir):
    origin = bidsroot / "sourcedata/ADIE983_beh_task.csv"
    saved_loc = convert_beh(origin, tmpdir,
                            "sub-ADIE983_ses-baseline", "mytask")
    assert saved_loc == tmpdir / "sub-ADIE983_ses-baseline_task-mytask_beh.tsv"

def test_name_physiobids():
    names = name_physiobids("sub-ADIE983_ses-baseline",
                            "mytask", signal_info)
    assert len(names) == len(signal_info)
    assert names[0] == "sub-ADIE983_ses-baseline_task-mytask_recording-ecg_physio"
    assert names[1] == "sub-ADIE983_ses-baseline_task-mytask_stim"

def test_save_physio(tmpdir):
    bidsnames = name_physiobids("sub-ADIE983_ses-baseline",
                            "mytask", signal_info)
    saved = save_physio(tmpdir, bidsnames,
                        signal_info, signals)
    assert len(saved) == len(bidsnames)
    assert saved[0] == str(tmpdir / bidsnames[0])
    assert saved[1] == str(tmpdir / bidsnames[1])

def test_smr_derivative(tmpdir):
    test_file = Path(__file__).parent /  "data/file.smr"
    sub_path, bn = gen_bidsbeh(tmpdir, "ADIE983", derivative="physio_smr")
    saved = smr_derivative(test_file, tmpdir,
                           "ADIE983", "mytask",
                           recording="ecg")
    assert saved == sub_path / f"{bn}_task-mytask_recording-ecg_physio.smr"
    assert saved.is_file() is True