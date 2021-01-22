from pathlib import Path


def get_bids_root_dir():
    return Path("__file__").parents[2]
