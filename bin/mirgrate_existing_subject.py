"""
Author: Will Strawson and Hao-Ting Wang, last updated 26-02-2021
Aim of this script is to create functions which:
(i) assimilate fMRI data from critchley_adie/wills_data/bids (or any outside directory) into
the critchley_adie/BIDS_data directory.
(ii) change the current session names to match those in BIDS_data/sub-*/
(i.e from dates to session labels)

Usage: Set variable 'subs' to a list of filepaths that point to each subject BIDs directory.

"""

# TODO: Allow user to specify the source directory (it's specified in path() function atm

from adie.migrate import *
import glob

subs = glob.glob(
    "/research/cisc2/projects/critchley_adie/wills_data/test_data/sub-*"
)
subs = [os.path.basename(i) for i in subs]

print("Subject directories to loop through:", subs)

progress = "n"
while progress != "y":
    progress = input("Would you like to continue? [y/n]")

for idx, sub in enumerate(subs):
    print(idx + 1, "/", len(subs))
    # F1 - Get paths
    src, dst = get_paths()

    # F2 - Match sub dirs
    try:
        src, dst = submatch(src, dst, sub)
    except Exception as e:
        print(e)
        continue

    # F3 - Match session dirs
    src, dst = sesmatch(src, dst)

    # F4 - Create sessions dictionary
    dir_pairs = sescreate(src, dst)

    # F5 - Create destination session directory
    make_ses_dir(dir_pairs)

    # F6 - Make neuro directory path
    make_neuro(dir_pairs)

    # F7 - Copy
    copydirs(dir_pairs)

    print(
        "---------------------------------------------------------------------"
    )
