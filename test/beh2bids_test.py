from pathlib import Path

from click.testing import CliRunner

from adie.scripts import beh2bids
from adie.scripts.beh2bids import main

bidsroot = Path(__file__).parent / "data/bids_test"

def test_beh2bids():
    runner = CliRunner()
    result = runner.invoke(beh2bids.main,
        ["--help",
         f"-s CONADIE999 -t mytask {str(bidsroot)}",
         f"-s CONADIE999 -t mytask -f *.csv {str(bidsroot)}",
         f"-s CONADIE999 -t mytask -f *.csv -p ecg {str(bidsroot)}",
         f"-s CONADIE989 -t mytask {str(bidsroot)}",
         f"-s ADIE999_F -t mytask -f **/*.csv {str(bidsroot)}",
        ])
    assert "Usage: main [OPTIONS] BIDS_ROOT" in result.output
    assert result.exit_code == 0

def test_find_file():
    exit = beh2bids.find_file("ADIE999_F", "*.csv",
          bidsroot / "sourcedata" / "faketask")
    assert exit == 1
    exit = beh2bids.find_file("ADIE999_F", "*.csv",
          bidsroot / "sourcedata" / "mytask")
    assert exit == 1

    ses = beh2bids.check_session("ADIE999_F",
      source_task=bidsroot / "sourcedata" / "mytask")
    for s in ses:
        exit = beh2bids.find_file(s, "*.csv",
            bidsroot / "sourcedata" / "mytask")
        assert exit == bidsroot / f"sourcedata/mytask/level1/anotherlevel/{s}/data.csv"

    ses = beh2bids.check_session("ADIE988_BL",
      source_task=bidsroot / "sourcedata" / "mytask")
    exit = beh2bids.find_file(ses[0], "*.csv",
        bidsroot / "sourcedata" / "mytask")
    assert exit == 1

    exit = beh2bids.find_file(ses[0], "**/*.csv",
        bidsroot / "sourcedata" / "mytask")
    assert exit == bidsroot / f"sourcedata/mytask/edge_case/level1/{ses[0]}/somedir/data.csv"

def test_check_session():
    exit = beh2bids.check_session("ADIE999_F",
      source_task=bidsroot / "sourcedata" / "faketask")
    assert exit == 1

    exit = beh2bids.check_session("ADIE999_F",
      source_task=bidsroot / "sourcedata" / "mytask")
    assert exit == ['ADIE999_BL', 'ADIE999F']

    exit = beh2bids.check_session("ADIE988_BL",
      source_task=bidsroot / "sourcedata" / "mytask")
    assert exit == ['ADIE988_BL']

    exit = beh2bids.check_session("ADIE999_F",
      source_task=bidsroot / "sourcedata" / "faketask")
    assert exit == 1

    exit = beh2bids.check_session("ADIE043_F",
      source_task=bidsroot / "sourcedata" / "mytask")
    assert exit == 1
