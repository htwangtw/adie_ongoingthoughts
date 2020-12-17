from adie.dataset import parseinfo, gen_bidsbeh, convert_beh

from pathlib import Path
import io


bidsroot = Path(__file__).parent / "data/bids_test"

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
    path, bn = gen_bidsbeh(bidsroot, "ADIE983", "baseline")
    assert path == Path(bidsroot) / "sub-ADIE983/ses-baseline/beh"
    assert path.is_dir() is True
    assert bn == "sub-ADIE983_ses-baseline"

    print("check file creation")
    path, bn = gen_bidsbeh(tmpdir, "ADIE983", "baseline")
    assert bn == "sub-ADIE983_ses-baseline"
    assert path == tmpdir / "sub-ADIE983/ses-baseline/beh"

def test_conver_beh(tmpdir):
    origin = bidsroot / "sourcedata/ADIE983_beh_task.csv"
    saved_loc = convert_beh(origin, tmpdir,
                            "sub-ADIE983_ses-baseline", "mytask")
    assert saved_loc == tmpdir / "sub-ADIE983_ses-baseline_task-mytask_beh.tsv"

