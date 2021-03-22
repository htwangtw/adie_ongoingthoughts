"""
#!/usr/bin/env/ python

Author: Will Strawson and Hao-Ting Wang, last updated 22-02-2021
Aim of this script is to convert CISC ID to ADIE ID in directory and file names


Usage:
When running from the command line, the user is asked to input the parent directory which
contains the subject directories they wish to convert.
"""

import pandas as pd
import os
import re
import shutil
import sys, os
from pathlib import Path
import glob

from .src.convert import *


# Script has to run from within critchely_adie/ cisc2 dir for the paths to work
# TODO: construct CISC2 file path
# TODO: change session- labels to be 'baseline' or 'intervention'

# Get path to ADIE dir - this is universal and should work for anyone running on the
# SN (Sussex neuroscience) server
adie_dir = ('/research/cisc2/projects/critchley_adie/')

# import conversion txt file
txtfile = os.path.join(adie_dir, 'BIDS_data/sourcedata/adie_idconvert.txt')
print ('Conversion txt file path =',txtfile)


# TODO: F7 - Chnage participants.tsv

# -------------- RUN FUNCTIONS -------------- #
# This bit will be in /test/ directory
# For now, just loop over one subject for testing purposes
# sourcery skip

# Allow user to input the subdirs
ok = 'n'
while ok == 'n':
    subdirs_parent = input("Input the path to the directory that contains the subject directories you wish to convert:\n")
    subdirs_srch = subdirs_parent+ '/sub-*'
    subdirs = glob.glob(subdirs_srch)
    print(subdirs_srch)
    print("The subject directories that will be converted are:")
    [print("{}".format(os.path.split(i)[1])) for i in subdirs]
    ok = input("do you wish to proceed? [n / y] \n")

print (ok)

# Loop through each subject
for sub in subdirs:
    # F5 - Store number of files in original directory
    numf_old = numfiles(sub)
    # Get dict
    rename = convert_dict(txtfile)
    # F1 - List sub directory for searching
    r = subpaths(sub)
    # F2 - Extract CISC ID from root name, and match with ADIE ID
    # If CISC ID not recognized, return to start of loop and processnext subject
    try:
        newid,cid = idmatch(r)
        print(newid,cid)
    except:
        print ("Error occured! Ignoring", sub)
        continue
    # F3 - Recreate directory sturcture, using new ID names
    newdir(newid,r)
    # F4 - Copy files from old to new structure, while renaming
    movefiles(sub,newid,cid)
    # F5 - Store number of files in new directory
    numf_new = numfiles(os.path.join(os.path.dirname(sub),newid))
    # F6 - Check if number of files in new sub dir is == to num files in original sub dir
    compare(numf_old,numf_new,sub)
    # Look prettier
    print ('\n','#####------------------- NEW SUBJECT DIRECTORY --------------------#####','\n')





