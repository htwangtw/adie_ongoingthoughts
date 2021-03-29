from pathlib import Path

from click.testing import CliRunner
import pytest

from adie.scripts import beh2bids
from adie.scripts.beh2bids import main
from adie.tests import get_test_data_path


bids_dir = Path(get_test_data_path()) / "adie_data"


@pytest.fixture
def runner():
    return CliRunner()


def test_beh2bids(runner):
    result = runner.invoke(
        beh2bids.main,
        ["-s", "CONADIE999", "-t", "mytask", "-p", "ecg", f"{str(bids_dir)}"],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        beh2bids.main,
        [
            "-s",
            "CONADIE999",
            "-t",
            "nosuchtask",
            "-p",
            "ecg",
            f"{str(bids_dir)}",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        beh2bids.main,
        ["-s", "ADIE999F", "-t", "mytask", "-p", "ecg", f"{str(bids_dir)}"],
    )
    assert result.exit_code == 0

    result = runner.invoke(beh2bids.main, ["--help"])
    assert "Usage: main [OPTIONS] BIDS_ROOT" in result.output
    assert result.exit_code == 0


def test_find_file():
    exit = beh2bids.find_file(
        "ADIE999_F", "*.csv", bids_dir / "sourcedata" / "faketask"
    )
    assert exit == 1
    exit = beh2bids.find_file(
        "ADIE999_F", "*.csv", bids_dir / "sourcedata" / "mytask"
    )
    assert exit == 1

    ses = beh2bids.check_session(
        "ADIE999_F", source_task=bids_dir / "sourcedata" / "mytask"
    )
    for s in ses:
        exit = beh2bids.find_file(
            s, "*.csv", bids_dir / "sourcedata" / "mytask"
        )
        assert (
            exit
            == bids_dir / f"sourcedata/mytask/level1/anotherlevel/{s}/data.csv"
        )

    ses = beh2bids.check_session(
        "ADIE988_BL", source_task=bids_dir / "sourcedata" / "mytask"
    )
    exit = beh2bids.find_file(
        ses[0], "*.csv", bids_dir / "sourcedata" / "mytask"
    )
    assert exit == 1

    exit = beh2bids.find_file(
        ses[0], "**/*.csv", bids_dir / "sourcedata" / "mytask"
    )
    assert (
        exit
        == bids_dir
        / f"sourcedata/mytask/edge_case/level1/{ses[0]}/somedir/data.csv"
    )


def test_check_session():
    exit = beh2bids.check_session(
        "ADIE999_F", source_task=bids_dir / "sourcedata" / "faketask"
    )
    assert exit == 1

    exit = beh2bids.check_session(
        "ADIE999_F", source_task=bids_dir / "sourcedata" / "mytask"
    )
    assert set(exit) == set(["ADIE999F", "ADIE999_BL"])

    exit = beh2bids.check_session(
        "ADIE988_BL", source_task=bids_dir / "sourcedata" / "mytask"
    )
    assert exit == ["ADIE988_BL"]

    exit = beh2bids.check_session(
        "ADIE999_F", source_task=bids_dir / "sourcedata" / "faketask"
    )
    assert exit == 1

    exit = beh2bids.check_session(
        "ADIE043_F", source_task=bids_dir / "sourcedata" / "mytask"
    )
    assert exit == 1
