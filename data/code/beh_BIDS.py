from pathlib import Path

import pandas as pd

from adie.dataset import *
from adie.spike import smr2array

bids_home = Path.home() / "projects/adie_ongoingthoughts/data"
sourcedata = "projects/adie_ongoingthoughts/data/sourcedata/nback_mindwadnering"
sourcedata = Path.home() / sourcedata

# create a dir for all subject id present
participant_info = []
for cur_file in sourcedata.glob("**/*mindwandering_MDES*_data.csv"):
    info = cur_file.parent.name
    sub, session, group = parseinfo(info)
    sub_path, base_name = gen_bidsbeh(bids_home, sub, session)
    target = convert_beh(cur_file, sub_path,
                         base_name, "nbackexpsampling")


# do the same for smr files
for cur_file in sourcedata.glob("**/*.smr"):
    sub, session, group = parseinfo(cur_file.parent.name)
    sub_path, basename = gen_bidsbeh(bids_home, sub, session)
    signal_info, signals = smr2array(str(cur_file))
    bidsnames = name_physiobids(basename, "nbackexpsampling", signal_info)
    _ = save_physio(sub_path, bidsnames, signal_info, signals)


# compile summary
participant_info = []
for p in bids_home.glob("sub-*/ses-*/"):
    ses = p.name.split("-")[-1]
    sub = p.parent.name.split("-")[-1]
    group = "control" if sub[0] == "C" else "patient"

    task_exist = len(list(p.glob("beh/*nbackexpsampling*"))) > 0
    physio_exist = len(list(p.glob("beh/*ecg*"))) > 0

    participant_info.append({"particpant_id": sub,
                             "session": ses,
                             "group": group,
                             "task_nbackexpsampling": int(task_exist),
                             "physio_nbackexpsampling": int(physio_exist)})

participant_info = pd.DataFrame(participant_info, index=None)
participant_info.to_csv(bids_home / "participants.tsv", index=False, sep="\t")