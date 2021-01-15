TASK=$1
BIDSDIR=$2

shopt -s globstar
subid=`ls ${BIDSDIR}/sourcedata/${TASK}/**/*ADIE*/ -d | awk -F "/" '{printf("%s\n", $(NF-1)); }'`

for sub in $subid; do
    beh2bids -s $sub -t $TASK -f "*mindwandering*_data.csv" -p "ecg" $BIDSDIR
done