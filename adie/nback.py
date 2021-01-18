from numpy.core.numeric import identity
import pandas as pd
from pathlib import Path

from .bids import parse_bids_filename, update_entity


accept_stimtype = ["MWQ", "NT", "TT", "END"]
identity_entity = ["sub", "ses", "run"]

def read_log(filepath: Path) -> dict:
    '''
    Read BIDS file path
    '''
    return {filepath.name : pd.read_csv(filepath, sep="\t")}

def extract_stimtype(data: pd.DataFrame, filename: str,
        stimtype: str, columns: list) -> pd.DataFrame:
    """
    Get trials with matching label under stimType
    """
    if stimtype not in accept_stimtype:
        raise ValueError(f"invalid {stimtype}, only accept {accept_stimtype}")

    parsed_fn = parse_bids_filename(filename)
    stimresp = data.query(f"stimType == '{stimtype}'")
    sliced = stimresp.loc[:, columns]
    return update_entity(sliced, identity_entity, parsed_fn)

# def extract_performance(self, parameter_list):
#     """
#     Get accuracy and reaction time
#     """
#     raise NotImplementedError

# def save_derivative(self, parameter_list):
#     """
#     Save extracted data
#     """
#     raise NotImplementedError