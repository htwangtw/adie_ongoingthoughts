![Test and coverage](https://github.com/htwangtw/adie_ongoingthoughts/workflows/Test%20and%20coverage/badge.svg)
[![codecov](https://codecov.io/gh/htwangtw/adie_ongoingthoughts/branch/main/graph/badge.svg?token=TM50FG36GZ)](https://codecov.io/gh/htwangtw/adie_ongoingthoughts)

# ADIE ongoing thought analysis

Authors: Hao-Ting Wang, Will Strawson

Last updated: 15-01-2021

As ADIE is a big dataset, it's the best to use Bash command to interact with the data.
We host it on the CISC storage voulme on Sussex HPC.

All tools were written based on [BIDSv1.4.1](https://bids-specification.readthedocs.io/en/v1.4.1/).

## Set-up your environment
Environment was tested under Ubuntu20.04 with Python >= 3.7.

We recommend running the project in a virtual environment.
```
virtualenv env -p /path/to/bin/python3.8
source env/bin/activate
pip install -i requirements.txt

# install ADIE data analysis aid
python setup.py
```

For developers:
```
virtualenv env -p /path/to/bin/python3.8
source env/bin/activate
pip install -i dev-requirements.txt
python setup.py
```

## Populate BIDS dataset

### Add a new participant
We created command line tool `beh2bids` to convert experiment log and physiology smr file.
To use this tool, place the new data under the relevant directory in `sourcedata`.
We only support conversion of CSV data log for now.

See more detail of this tool:
```
$ beh2bids --help

Usage: beh2bids [OPTIONS] BIDS_ROOT

  bids_root: path to the root direcotry of BIDS dataset

Options:
  -t, --task TEXT     Task directory name unders sourcedata.
  -s, --subject TEXT  ADIE subject identifier (ADIE??? / CONADIE??? or
                      suffix with session such as "ADIE???BL")

  -f, --behfile TEXT  Behavioural data log file name pattern
                      [default: *.csv]

  -p, --physio TEXT   physiology recording type, such as ecg, pulseox.
                      Set to None if no physiology data is present.

  --help              Show this message and exit.
```

### Batch process new experiment data
Please find cluster job script `bin/populate_nback.sh` and use it as a template.
`bin/populate_nback.sh` is compatible with Sussex HPC scheduler SGE.

### fMRI data
WIP