import sys

from os.path import basename
import click

import re
from pathlib import Path

from ..dataset import (parseinfo, gen_bidsbeh,
            convert_beh, smr_derivative, save_physio)
from ..spike import smr2array

@click.command()
@click.argument('task',
    help='Task directory name unders sourcedata.')
@click.argument('adiesub',
    help='ADIE subject identifier (ADIE??? / CONADIE??? or suffix with session such as "ADIE???BL")')
@click.argument('bids_root', type=click.Path(exists=True),
    help='The root direcotry of BIDS dataset')
@click.option('--behfile', '-f', 'file_pattern', default="*.csv", show_default=True,
    help="Behavioural data log file name pattern")
@click.option('--physio', '-p', default=None, show_default=True,
    help="physiology recording type, such as ecg, pulseox. Set to None if no physiology data.")

def main(adiesub: str, task:str , bids_root:str,
          file_pattern: str, physio:str or None):
    bids_root = Path(bids_root)
    source_task = bids_root / "sourcedata" / task

    session_list = check_file(adiesub, task, source_task)
    if session_list == 1:
        return

    click.echo(f"found {len(session_list)} sessions associated with {adiesub}")
    while session_list:
        cur_ses = session_list.pop()
        click.echo(cur_ses)
        sub, session, _ = parseinfo(cur_ses)
        sub_path, base_name = gen_bidsbeh(bids_root, sub, session)

        cur_beh = find_file(cur_ses, file_pattern, source_task)
        beh_path = convert_beh(cur_beh[0], sub_path,
                                base_name, task)
        click.echo(f"f{beh_path} created")

        if physio:
            cur_physio = find_file(cur_ses, "*.smr", source_task)
            physio_path = save_physio(sub_path, base_name, task, cur_physio)
            click.echo(f"f{physio_path} created")

            der_smr = smr_derivative(cur_physio, bids_root, sub, task,
                            session=session, recording=physio)
            click.echo(f"f{der_smr} created")

def find_file(cur_ses, file_pattern, source_task):
    cur_file = source_task.rglob(f"{cur_ses}/ {file_pattern}")
    if len(cur_file) == 1:
        return cur_file
    click.echo(f"found none or too many match for {file_pattern} in {cur_ses}; use batter `file_pattern`")
    return 1

def check_file(adiesub: str, task: str, source_task: Path) -> list(str):
    sub, _, _ = parseinfo(adiesub)  # will look for all sessions
    click.echo(f"look for subject {sub} in sourcedata {task}")
    if not source_task.is_dir():
        click.echo(f"{task} not in sourcedata. Wrong task name?")
        return 1
    session_list = [p.name for p in source_task.glob(f"**/{sub}*/") if p.is_dir()]
    if not session_list:
        click.echo(f"{sub} not in {task}. Wrong subject ADIE ID?")
        return 1
    return session_list

if __name__ == "__main__":
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("convert ADIE project behavioural data to BIDS")
    main()