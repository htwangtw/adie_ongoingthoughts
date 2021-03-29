from numpy.core.fromnumeric import mean
from numpy.core.numeric import identity
import pandas as pd
from pathlib import Path

from .bids import parse_bids_filename, update_entity


accept_stimtype = ["MWQ", "NT", "TT", "END"]
identity_entity = ["sub", "ses", "run"]


def read_log(filepath: Path) -> dict:
    """
    Read BIDS file path
    """
    file = pd.read_csv(filepath, sep="\t")
    parsed_fn = parse_bids_filename(filepath.name)
    return update_entity(file, identity_entity, parsed_fn)


def extract_stimtype(
    data: pd.DataFrame, stimtype: str, columns: list
) -> pd.DataFrame:
    """
    Get trials with matching label under stimType
    """
    if stimtype not in accept_stimtype:
        raise ValueError(f"invalid {stimtype}, only accept {accept_stimtype}")
    get = columns.copy()
    get += ["participant_id"]
    get += [i for i in identity_entity if i in data.columns]
    stimresp = data.query(f"stimType == '{stimtype}'")
    return stimresp.loc[:, get]


def compile_probes(data):
    """
    Get thought probes
    """
    # disgusting one liner to get all thought probes
    columns = [
        "StimIndex",
        "nBack",
        "fixStart",
        "stimStart",
        "mwType",
        "keyResp",
        "respRT",
    ]
    data = extract_stimtype(data, "MWQ", columns)
    probes = _split_probes(data)
    nback = _find_probe_condition(data)
    probe_time = _get_probe_time(data)
    probes = pd.concat([nback, probe_time, probes], axis=1)
    probes.index.name = "probe_index"
    return probes


def compile_ses(data):
    """
    Get thought probes at session end
    """
    # disgusting one liner to get all thought probes
    columns = ["mwType", "keyResp"]
    data = extract_stimtype(data, "END", columns).reset_index()
    subj_info = data.loc[:, ["participant_id", "ses"]]
    col = data["mwType"].values.tolist() + subj_info.columns.tolist()
    val = data["keyResp"].values.tolist() + subj_info.loc[0, :].values.tolist()
    return pd.DataFrame(val, index=col).T.set_index(["participant_id", "ses"])


def compile_performance(data):
    """
    Get reaction time and accuracy
    """
    columns = ["nBack", "Ans", "keyResp", "respRT"]
    task_perf = extract_stimtype(data, "TT", columns)
    # get correct bool
    task_perf["acc"] = (task_perf["Ans"] == task_perf["keyResp"]).apply(int)
    cond = pd.pivot_table(
        task_perf,
        index=["participant_id", "ses", "nBack"],
        values=["acc", "respRT"],
    )
    overall = pd.pivot_table(
        task_perf, index=["participant_id", "ses"], values=["acc", "respRT"]
    )
    overall["nBack"] = "overall"
    return pd.concat([cond.reset_index(), overall.reset_index()])


def save_derivative(self, parameter_list):
    """
    Save extracted data
    """
    raise NotImplementedError


def _split_probes(data):
    probes = [
        entry.loc[:, ["keyResp"]].rename({"keyResp": mwtype}, axis=1)
        for mwtype, entry in data.groupby("mwType")
    ]
    return pd.concat([p.reset_index(drop=True) for p in probes], axis=1)


def _find_probe_condition(data):
    return data.query("mwType == 'Focus'")[
        ["participant_id", "ses", "nBack"]
    ].reset_index(drop=True)


def _find_probe_index(data):
    idx_start = data.query("mwType == 'Focus'").index
    return idx_start, idx_start + 12


def _get_probe_time(data):
    idx_start, idx_end = _find_probe_index(data)
    probe_start = data.loc[idx_start, "stimStart"].reset_index(drop=True)
    prob_end = data.loc[idx_end, ["stimStart", "respRT"]].reset_index(
        drop=True
    )
    prob_end = prob_end.sum(axis=1)
    prob_end.name = "stimEnd"
    return pd.concat([probe_start, prob_end], axis=1)
