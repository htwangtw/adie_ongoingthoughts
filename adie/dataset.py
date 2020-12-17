import re
import os
import json

from pathlib import Path

import pandas as pd


session_check = {
    "": "baseline",
    "BL": "baseline",
    "F": "3mf",
    "FY": "1yf"
    }

physio_labels = ["ecg", "respiratory", "cardiac"]

def parseinfo(info: str) -> (str, str, str):
    """
    parse ADIE project data directory to subject info

    input
    -----
    info: str

    output
    ------
     sub, session, group: str
    """
    p = re.search("((CON)?ADIE[0-9]*)(_)?([A-Z]*)", info)
    sub = p.group(1)
    group = "control" if p.group(2) == "CON" else "patient"
    session = session_check[p.group(4)]
    return sub, session, group


def gen_bidsbeh(bidsroot: Path or str,
                sub: str, session: str) -> (Path, str):
    """
    Generate behavioural data file path
    """

    if type(bidsroot) ==str:
        bidsroot = Path(bidsroot)
    base_name = f"sub-{sub}_ses-{session}"
    dir_template = f"sub-{sub}/ses-{session}/beh"
    new_sub = Path(bidsroot / dir_template)
    if new_sub.is_dir():
        print(f"""behavioural data directory exist:
sub-{sub}, ses-{session}""")
    else:
        print(f"""behavioural data directory created:
sub-{sub}, ses-{session}""")
        os.makedirs(new_sub)
    return new_sub, base_name

def convert_beh(original: Path, target: Path,
               basename: str, label: str) -> Path:
    """
    save general behavioural data to BIDS spec beh file
    """
    df = pd.read_csv(original, header=0)
    target_file = f"{basename}_task-{label}_beh.tsv"
    df.to_csv(target / target_file, sep= "\t", index=False)
    return target / target_file


def save_physio(filename: Path or str, basename: str,
                signal_info: list, signals: list) -> path:
    """
    save converted spike physio data to BIDS spec beh file
    """
    if filename is Path:
        filename = str(filename)

    for d, s in zip(signal_info, signals):
        recording = signal_info["Columns"][0]
        if recording in physio_labels:
            suffix = "physio"
            physio_basename = f"{base_name}_task-{label}_recording-{recording}_{suffix}"
        else:
            suffix = "stim"
            physio_basename = f"{base_name}_task-{label}_{suffix}"
        # save signal (`s`) into tsv, compressed
        # save dict (`d`) into json
