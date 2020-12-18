from adie.spike import smr2array

from pathlib import Path
import numpy as np


def test_smr2array():
    test_file = Path(__file__).parent /  "data/file.smr"
    test_file = str(test_file)
    out = smr2array(test_file)
    assert type(out) == tuple
    assert type(out[0]) == list
    assert type(out[0][0]) == dict
    assert type(out[1][0]) == np.ndarray
    assert out[1][0].shape[0] == 790040

