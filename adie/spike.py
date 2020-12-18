from pathlib import Path
import re
import json

import numpy as np

from neo.io import Spike2IO

def smr2array(filename: str) -> (list, list):
    """
    helper function to read signal from .smr file (Spike2) for the current task
    This function will have to be modified at a project by project basis
    """
    p = Spike2IO(filename=filename, try_signal_grouping=False)
    assert p.block_count() == 1
    s = p.read()[0].segments[0]
    keyboard = s.events[0]  # this is empty for the nback task
    analog_channels = s.analogsignals


    signals = []
    signal_info = []
    for i, ac in enumerate(analog_channels):
        signal_dict = {"SamplingFrequency": p.get_signal_sampling_rate([i]),
                        "StartTime": 0.0,
                        "Columns": []}
        signal = ac.as_array()
        # if signal.shape[0] > signal.shape[1]:
        #     signal = signal.reshape((signal.shape[1], signal.shape[0]))
        signal_dict["Columns"].append(ac.name.lower())
        signal_dict[ac.name] = {"Unit": "arbitrary"}

        signals.append(signal)
        signal_info.append(signal_dict)

    return signal_info, signals