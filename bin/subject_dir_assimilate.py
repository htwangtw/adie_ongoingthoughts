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

# F1 - retrieve the relevent universal paths
# source directory - wills_data/bids
# destination directory - BIDS_data/

# F2 - match individuals subjects directories in source and destination

# F3 - match session level directories 
# earliest date == what session label? baseline? first follow up? 

# F4 - create session level destination directorys with new label name 
# (won't need ot create  new session dirs if behavioural assessments occured at the same time as neuroimaging
# as sesssion dirs for beh/ already exist - study semantic check)

# F5 - create 'neuro' dir inside session dir

# F5 - copy files from source to dest 
# inside correct session dir, and inside new neuro dir



