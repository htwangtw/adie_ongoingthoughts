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

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

from adie.convert import *

# Get path to ADIE dir - this is universal and should work for anyone running on the
# SN (Sussex neuroscience) server
adie_dir = ('/research/cisc2/projects/critchley_adie/')

# import conversion txt file
txtfile = os.path.join(adie_dir, 'BIDS_data/sourcedata/adie_idconvert.txt')
print ('Conversion txt file path =',txtfile)

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

# Loop through each subject
for sub in subdirs:
    # F5 - Store number of files in original directory
    numf_old = numfiles(sub)
    # Get dict
    rename = convert_dict(txtfile)
    # consolodate as string 
    print('rename var=',rename)
    r = str(sub)
    print('r:',r)
    # F2 - Extract CISC ID from root name, and match with ADIE ID
    # If CISC ID not recognized, return to start of loop and processnext subject
    try:
        newid,cid = idmatch(r, rename)
        print(newid,cid)
    except Exception as e:
        print (e)
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






