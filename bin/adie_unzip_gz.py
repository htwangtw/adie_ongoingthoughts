from pathlib import Path
import glob
import os
import pandas as pd

path = Path.cwd() # Or path/to/adie/BIDS_DATA
filepath = os.path.join("sub-*", "ses-b*", "beh", "*ecg_physio.tsv.gz") # ses-b* can be changed to ses-o* 
data = os.path.join(path, filepath)
files = glob.glob(data)

for i in files:
    df = pd.read_csv(i, sep="\t", compression="gzip")
    i = i.split(os.sep)
    subid = i[-4]
    df.to_csv(subid + "_ecg", sep='\t', index=False)
