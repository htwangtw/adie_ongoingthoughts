#!/usr/bin/env/ python 
#coding=utf-8
"""
Author: Will Strawson and Hao-Ting Wang, last updated 26-02-2021
Aim of this script is to: 
(i) assimilate fMRI data from critchley_adie/wills_data/bids into 
the critchley_adie/BIDS_data directory.
(ii) change the current session names to match those in BIDS_data/sub-*/
(i.e from dates to session labels)

Usage:

"""

import os
import glob

# F1 - retrieve the relevent universal paths
def paths():
    base = 'research/cisc2/projects/critchley_adie/'
    # source directory - wills_data/bids
    src = os.path.join(base,'wills_data/bids/')
    # destination directory - BIDS_data/
    dst = os.path.join(base,'BIDS_data/')
    return src, dst

# F2 - match individuals subjects directories in source and destination
def sub_match(src,dst,sub):
    # get subject directory in src and dets
    sub_src = os.path.join(src,sub)
    sub_dest os.path.join(dest,sub)
    if os.path.exists(sub_src) == False:
        print('ERROR: Source subject directory not found ({})'.format(sub_src))
    elif os.path.exists(sub_dest) == False:
        print('ERROR: Source subject directory not found ({})'.format(sub_dest))

    


# F3 - match session level directories 
# earliest date == what session label? baseline? first follow up? 

# F4 - create session level destination directorys with new label name 
# (won't need ot create  new session dirs if behavioural assessments occured at the same time as neuroimaging
# as sesssion dirs for beh/ already exist - study semantic check)

# F5 - create 'neuro' dir inside session dir

# F5 - copy files from source to dest 
# inside correct session dir, and inside new neuro dir



