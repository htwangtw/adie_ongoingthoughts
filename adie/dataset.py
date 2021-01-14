import re
import os
from shutil import copyfile
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
        ADIE participant number

    output
    ------
     sub, session, group: str
        BIDS compatable ADIE information

    """
    p = re.search("((CON)?ADIE[0-9]*)(_)?([A-Z]*)", info)
    sub = p.group(1)
    group = "control" if p.group(2) == "CON" else "patient"
    session = session_check[p.group(4)]
    return sub, session, group


def gen_bidsbeh(bidsroot: Path or str,
                sub: str, session: str = None,
                derivative: str = None) -> (Path, str):
    """
    Generate behavioural data file path

    input
    -----
    bidsroot:
        BIDS directory
    sub:
        subject ID
    session:
        session label
    derivative:
        BIDS derivative name (default None)

    output
    ------
    new_sub, base_name: str
        BIDS subject directory and BIDS subject file base name
    """

    if type(bidsroot) ==str:
        bidsroot = Path(bidsroot)

    if session:
        base_name = f"sub-{sub}_ses-{session}"
        dir_template = f"sub-{sub}/ses-{session}/beh"
    else:
        base_name = f"sub-{sub}"
        dir_template = f"sub-{sub}/beh"

    if derivative:
        dir_template = f"derivatives/{derivative}/{dir_template}"

    new_sub = Path(bidsroot / dir_template)
    if new_sub.is_dir():
        print(f"""behavioural data directory exist: {base_name}""")
    else:
        print(f"""behavioural data directory created: {base_name}""")
        os.makedirs(new_sub)
    return new_sub, base_name

def convert_beh(original: Path, target: Path,
               basename: str, label: str) -> Path:
    """
    save general behavioural data to BIDS spec beh file
    """
    target_file = f"{basename}_task-{label}_beh.tsv"
    if (target / target_file).exists():
        print(f"file exist: {str(target / target_file)}")
    else:
        print("convert to BIDS")
        df = pd.read_csv(original, header=0)
        df.to_csv(target / target_file, sep= "\t", index=False)
    return target / target_file


def name_physiobids(basename: str, task: str, signal_info: list) -> list:
    """
    generate physiology data name

    input
    -----
    basename:
        BIDS subject file base name
    task:
        task label
    signal_info:
        list of json containing meta data of the signal

    output
    ------
    names:
        list of physio data name
    """
    names = []
    for d in signal_info:
        recording = d["Columns"][0]
        if recording in physio_labels:
            suffix = "physio"
            physio_basename = f"{basename}_task-{task}_recording-{recording}_{suffix}"
        else:
            suffix = "stim"
            physio_basename = f"{basename}_task-{task}_{suffix}"
        names.append(physio_basename)
    return names


def save_physio(target: Path, bidsnames: list,
                signal_info: list, signals: list) -> list:
    """
    save converted spike physio data to BIDS spec beh file

    input
    -----
    target:
        target directory
    bidsnames:
        bids compatable file name
    signal_info:
        list of json containing meta data of the signal

    signals:
        list containing the signal in 1d numpy arrays

    output
    ------
    names:
        list of saved physio data path
    """
    saved = []
    for n, d, s in zip(bidsnames, signal_info, signals):
        s = pd.DataFrame(s, index=None, columns=d["Columns"])
        s.to_csv(target / f"{n}.tsv.gz", sep="\t", compression="gzip")
        with open(target / f"{n}.json", 'w') as f:
                json.dump(d, f, indent=2)
        saved.append(str(target / f"{n}"))

    return saved

def smr_derivative(origin: Path, bidsroot: Path or str,
                sub: str, task: str, recording: str,
                session: str = None,
                ) -> Path:
    """
    organise the smr files in BIDS for people who
    prefer to use original spike files

    input
    -----
    origin:
        path to the smr file
    target:
        path to the derivative directory
    basename:
        BIDS basename
    task:
        associated task name
    recording:
        optional, type of recording

    output
        path to the renamed file
    ------
    """
    target, basename = gen_bidsbeh(bidsroot, sub, session, derivative="physio_smr")
    target_file = f"{basename}_task-{task}_recording-{recording}_physio.smr"
    copyfile(origin, target / target_file)
    return target / target_file