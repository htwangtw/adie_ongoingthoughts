![Test and coverage](https://github.com/htwangtw/adie_ongoingthoughts/workflows/Test%20and%20coverage/badge.svg)
[![codecov](https://codecov.io/gh/htwangtw/adie_ongoingthoughts/branch/main/graph/badge.svg?token=TM50FG36GZ)](https://codecov.io/gh/htwangtw/adie_ongoingthoughts)

# ADIE data curation tools

Authors: Hao-Ting Wang, Will Strawson, Joel Patchitt

Last updated: 15-01-2021

As ADIE is a big dataset, it's the best to use Bash command to interact with the data.
We host it on the CISC storage voulme on Sussex HPC.

All tools were written based on [BIDSv1.4.1](https://bids-specification.readthedocs.io/en/v1.4.1/).

## Set-up your environment
Environment was tested under Ubuntu20.04 with Python >= 3.7.

We recommend running the project in a virtual environment.

### Linux
```
cd /path/to/this/repo/
virtualenv env -p /path/to/bin/python3.8
source env/bin/activate
pip install -r requirements.txt

# install ADIE data analysis aid
python setup.py
```
After setup for the first time, you need to activate the enviroment to use this project.
```
cd /path/to/this/repo/
source env/bin/activate
```
To deactivate:
```
deactivate
```

For developers:
```
virtualenv env -p /path/to/bin/python3.8
source env/bin/activate
pip install -r dev-requirements.txt
python setup.py
```

## Populate BIDS dataset

All scripts are under `bin`.
Packaged analysis module `adie` is in directory of the same name.
If you follow the setup instruction, you should be able to use the `adie` module as a normal python module in the project environment after sourcing the virtual environment.

```
cd /path/to/this/repo/
source env/bin/activate
```

I am considering to publish it as a standard library for the ease of use.
If you want to work on it, let me know!

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

## Questions, bugs related to this tool
Please let me know by opening an [issue](https://github.com/htwangtw/adie_ongoingthoughts/issues)!

## Contribution guidelines
Please have a look at nibable's [contribution guidelines](https://nipy.org/nibabel/devel/devguide.html). I found them really useful so nor bothered to write my own. These guidelines are designed to make it as easy as possible to get involved. If you have any questions that aren't discussed in the documentation, or it's difficult to find what you're looking for, please let me know by opening an [issue](https://github.com/htwangtw/adie_ongoingthoughts/issues)!
