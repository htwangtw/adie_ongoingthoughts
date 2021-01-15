import re
import pandas as pd

bids_pattern = "(sub-[A-Za-z0-9]*)_(ses-[A-Za-z0-9]*_)?(task-[A-Za-z0-9]*_)(acq-[A-Za-z0-9]*_)?(ce-[A-Za-z0-9]*_)?(rec-[A-Za-z0-9]*_)?(dir-[A-Za-z0-9]*_)?(run-[0-9]*_)?(mod-[A-Za-z0-9]*_)?(echo-[0-9]*_)?(recording-[A-Za-z0-9]*_)?(proc-[A-Za-z0-9]*_)?(space-[A-Za-z0-9]*_)?(split-[A-Za-z0-9]*_)?([a-z]*).([a-z.]*)"

def parse_bids_filename(filename: str) -> dict:
    """
    parse BIDS filename (sub-*_ses-*_*.ext) into separate entities

    input
    -----
    filename:
        BIDS file name including the file extention

    output
    ------
        dict
    """
    parsed = {}
    results = list(re.search(bids_pattern, filename).groups())
    parsed["ext"] = results.pop()
    while results:
        item = results.pop()
        if item is not None:
            parsed.update(_parse_segment(item))
    return parsed

def _parse_segment(item: str) -> dict:
    if "-" not in item:
        return {"suffix": item}
    item = item.split("_")[0].split("-")
    return {item[0]: item[1]}

def update_entity(df: pd.DataFrame, entity: str or list,
        parsed_filename: dict) -> pd.DataFrame:
    """
    fill columns with BIDS entity information in a tsv file
    such as participant_id, session, run, etc
    """
    update = df.copy()
    if type(entity) is str:
        entity = [entity]

    while entity:
        e = entity.pop()
        if e == "sub":
            update["participant_id"] = f"sub-{parsed_filename[e]}"
        elif e in parsed_filename:
            update[e] = f"{parsed_filename[e]}"
    return update