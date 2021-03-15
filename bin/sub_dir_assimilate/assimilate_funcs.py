#!/usr/bin/env/ python 
#coding=utf-8
"""
Author: Will Strawson and Hao-Ting Wang, last updated 26-02-2021
Aim of this script is to create functions which: 
(i) assimilate fMRI data from critchley_adie/wills_data/bids into 
the critchley_adie/BIDS_data directory.
(ii) change the current session names to match those in BIDS_data/sub-*/
(i.e from dates to session labels)

"""

import os
import glob
from subprocess import call

# F1 - retrieve the relevent universal paths
def paths():
    base = '/research/cisc2/projects/critchley_adie/'
    # source directory - wills_data/bids
    src = os.path.join(base,'wills_data/bids/')
    # destination directory - BIDS_data/
    dst = os.path.join(base,'BIDS_data/')
    return src, dst

# F2 - match individuals subjects directories in source and destination
def submatch(src,dst,sub):
    # get subject directory in src and dest
    sub_src = os.path.join(src,sub)
    sub_dst = os.path.join(dst,sub)
    if os.path.exists(sub_src) == False:
        print('ERROR: Source subject directory not found ({})'.format(sub_src))
         
    if os.path.exists(sub_dst) == False:
        print('ERROR: Source subject directory not found ({})'.format(sub_dst))
        
    else:
        return sub_src, sub_dst
        #print (sub_src, sub_dst)

# F3 - match session level directories 
def sesmatch(sub_src,sub_dst):
    # how many src session dirs
    src_sessions = glob.glob(os.path.join(sub_src,'ses-*'))
    print (src_sessions)
    ses_dates = [os.path.basename(i) for i in src_sessions]
    # how many dst session dirs
    dst_sessions = glob.glob(os.path.join(sub_dst,'ses-*'))
    print (dst_sessions)
    ses_names = [os.path.basename(i) for i in dst_sessions]
    
    print ('fMRI sessions: {}'.format(ses_dates))
    print ('Behavioural sessions: {}'.format(ses_names))

    return src_sessions, dst_sessions

# F4 - create session level destination directorys paths with new label name 
def sescreate(src_sessions,dst_sessions):
    # pair up each src session with dst session using dict 

    # extract baseline session path 
    baseline_ses = [i for i in dst_sessions if 'baseline' in i]
    try:
        baseline_ses = baseline_ses[0]
    # if baseline session path doesn't exist (e.g if no behavioural assessment done at baseline), consruct filepath
    except: 
            baseline_ses = os.path.join(os.path.dirname(dst_sessions[0]),'baseline')
            print ('No existing baseline directory - creating one')

    # if there's only one src_session, dst = baseline/
    if len(src_sessions) == 1:
        dir_pairs = {src_sessions[0]:baseline_ses}
    
    # if there's two src_sessions, dsts = baseline/ and posttraining/
    elif len(src_sessions) == 2:
        # create posttraining dir
        pt_ses = os.path.join(os.path.dirname(baseline_ses),'posttraining')
        dir_pairs = {src_sessions[0]:baseline_ses, src_sessions[1]:pt_ses}

    
    return dir_pairs    

# F5 - make session level directory (if doesn't already exist)

def make_ses_dir(dir_pairs):
    # If destiation session directory doesn't exists, make it.
    for k,v in dir_pairs.items():
        if os.path.exists(dir_pairs[k]) == False:
            print ('Creating the following directory:',dir_pairs[k])
            os.mkdir(dir_pairs[k])
        elif os.path.exists(dir_pairs[k]) == True:
            print ('Following directory already exists:', dir_pairs[k])


# F6 - create 'neuro' dir inside session dir

def make_neuro(dir_pairs):
    for k,v in dir_pairs.items():
        dir_pairs[k] = os.path.join(v,'neuro')
        if os.path.exists(dir_pairs[k]) == False:
            print ('neuro/ does not exist yet - creating now')
            os.mkdir(dir_pairs[k])
        elif os.path.exists(dir_pairs[k]) == True:
            print ('neuro/ already exists')

    
# F7 - copy files from source to dest 
def copydirs(dir_pairs):
    for k,v in dir_pairs.items():
        # copy files inside the session directory, not the session directory itself due to date-based name
        sources = glob.glob(k+'/*')
        destination = v
        if len(os.listdir(v)) == 0:
            print('Copying:',sources,'\n','to:',destination)
            # copy all files in sources list 
            [call(['cp','-a','-R',i,destination]) for i in sources]          
        else:
            print('Destination directory not empty',os.listdir(v))





