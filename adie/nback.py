import pandas as pd
from pathlib import Path

def read_log(filepath: Path) -> pd.DataFrame:
    '''
    Read BIDS file path
    '''
    return pd.read_csv(filepath, sep="\t")

def extract_probes(self, parameter_list):
    """
    Get thought probes
    """
    raise NotImplementedError

def extract_performance(self, parameter_list):
    """
    Get accuracy and reaction time
    """
    raise NotImplementedError

def save_derivative(self, parameter_list):
    """
    Save extracted data
    """
    raise NotImplementedError