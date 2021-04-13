"""
Author: Will Strawson and Hao-Ting Wang, last updated 26-02-2021
Aim of this script is to create functions which:
(i) assimilate fMRI data from critchley_adie/wills_data/bids (or any outside directory) into
the critchley_adie/BIDS_data directory.
(ii) change the current session names to match those in BIDS_data/sub-*/
(i.e from dates to session labels)

Usage: Set variable 'subs' to a list of filepaths that point to each subject BIDs directory.

"""

import os
from adie import migrate
import glob

subs = glob.glob(
    "/research/cisc2/projects/critchley_adie/wills_data/bids/sub-*"
)
subs = [os.path.basename(i) for i in subs]
base = "/research/cisc2/projects/critchley_adie/"
base_src = os.path.join(base, "wills_data/bids/")
base_dst = os.path.join(base, "BIDS_data/")

for idx, sub in enumerate(subs):
    print(idx + 1, "/", len(subs))
    try:
        src, dst = migrate.submatch(base_src, base_dst, sub)
    except:
        print("error when matching sub dirs {}, skip".format(sub))
        continue
    src, dst = migrate.sesmatch(src, dst)
    dir_pairs = migrate.sescreate(src,dst,sub)
    migrate.make_ses_dir(dir_pairs)
    #migrate.make_neuro(dir_pairs)
    migrate.copydirs(dir_pairs)

    print(
        "---------------------------------------------------------------------"
    )
