#!/bin/bash
#$ -N populate_nback
#$ -o /home/$USER/logs

TASK=$1
BIDSDIR=$2

cd ${BIDSDIR}/code
source env/bin activate

pip install ${BIDSDIR}/code/

shopt -s globstar
subid=`ls ${BIDSDIR}/sourcedata/${TASK}/**/*ADIE*/ -d | awk -F "/" '{printf("%s\n", $(NF-1)); }'`

for sub in $subid; do
    beh2bids -s $sub -t $TASK -f "*mindwandering*_data.csv" -p "ecg" $BIDSDIR
done