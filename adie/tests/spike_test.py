import os
import numpy as np

from adie.spike import smr2array
from adie.tests import get_test_data_path



def test_smr2array():
    test_file = os.path.join(get_test_data_path(), "file.smr")
    out = smr2array(test_file)
    assert type(out) == tuple
    assert type(out[0]) == list
    assert type(out[0][0]) == dict
    assert type(out[1][0]) == np.ndarray
    assert out[1][0].shape[0] == 790040