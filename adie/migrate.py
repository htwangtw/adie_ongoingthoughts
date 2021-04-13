#!/usr/bin/env/ python
# coding=utf-8
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

def get_paths():
    """retrieve the relevent universal paths"""
    base = "/research/cisc2/projects/critchley_adie/"
    # source directory - wills_data/bids
    src = os.path.join(base, "wills_data/bids/")
    # destination directory - BIDS_data/
    dst = os.path.join(base, "BIDS_data/")
    return src, dst


def submatch(src, dst, sub):
    """rmatch individuals subjects directories in source and destination"""
    # get subject directory in src and dest
    sub_src = os.path.join(src, sub)
    sub_dst = os.path.join(dst, sub)
    if os.path.exists(sub_src) == False:
        print("ERROR: Source subject directory not found ({})".format(sub_src))

    else:
        return sub_src, sub_dst
        # print (sub_src, sub_dst)


def sesmatch(sub_src, sub_dst):
    """match session level directories"""
    # how many src session dirs
    src_sessions = glob.glob(os.path.join(sub_src, "ses-*"))
    #print(src_sessions)
    ses_dates = [os.path.basename(i) for i in src_sessions]
    # how many dst session dirs
    dst_sessions = glob.glob(os.path.join(sub_dst, "ses-*"))
    #print(dst_sessions)
    ses_names = [os.path.basename(i) for i in dst_sessions]

    print("fMRI sessions: {}".format(ses_dates))
    print("Behavioural sessions: {}".format(ses_names))

    return src_sessions, dst_sessions


def sescreate(src_sessions, dst_sessions, sub):
    """create session level destination directorys paths with new label name"""
    # pair up each src session with dst session using dict
    session_ids = ["baseline", "posttraining"]
    dir_pairs = {}
    
    # I assume you have maximum of two sessions in source and destination
    assert len(dst_sessions) <= 2 
    assert len(src_sessions) <= 2 
    # create subject dir if not exist
    subdir = os.path.join('/research/cisc2/projects/critchley_adie/BIDS_data/',sub)
    if not os.path.exists(subdir):
        print(f'CREATING: {subdir}')
        os.mkdir(subdir)
    else:
        print(f'{sub}: subject dir already exists')

    # ensure length of src_session and dst_sessions matches 
    checked_dst_sessions = []
    for ses in session_ids[:len(src_session)]:
        dst = _check_dst(dst_sessions, ses)
        checked_dst_sessions.append(dst)
    return {src: dst for src, dst in zip(src_sessions, checked_dst_sessions)}


def _create_dst_ses(subdir, session):
    """create destination session dir"""
    dst = os.path.join(subdir, f'ses-{session}')
    print ('Making session:', dst)
    os.mkdir(dst)
    return dst


def _check_dst(dst_sessions, session):
    """
    Return destination path for a given session
    create destination if path not exist.
    
    Parameters
    ----------
    dst_sessions: list of str or empty list
        List of BIDS session path in desitination directory
    
    session: str
        Session label.     
    """
    current_ses = None
    for dst in dst_sessions:
        if session in dst:
            current_ses = dst

    if not current_ses:
        print(f"No existing {session} directory - creating one")
        sub_dir = os.path.dirname(dst_sessions[0])
        current_ses = _create_dst_ses(subdir, session)
    return current_ses

def make_ses_dir(dir_pairs):
    """make session level directory (if doesn't already exist)"""
    # If destiation session directory doesn't exists, make it.
    for k, v in dir_pairs.items():
        if os.path.exists(dir_pairs[k]) == False:
            print("Creating the following directory:", dir_pairs[k])
            os.mkdir(dir_pairs[k])
        elif os.path.exists(dir_pairs[k]) == True:
            print("Following directory already exists:", dir_pairs[k])


def make_neuro(dir_pairs):
    """create 'neuro' dir inside session dir"""
    for k, v in dir_pairs.items():
        dir_pairs[k] = os.path.join(v, "neuro")
        if os.path.exists(dir_pairs[k]) == False:
            print("neuro/ does not exist yet - creating now")
            os.mkdir(dir_pairs[k])
        elif os.path.exists(dir_pairs[k]) == True:
            print("neuro/ already exists")

def copydirs(dir_pairs):
    """copy files from source to dest"""
    for k, v in dir_pairs.items():
        # copy files inside the session directory, not the session directory itself due to date-based name
        sources = glob.glob(k + "/*")
        destination = v
        # only copy if files not previous copies 
        isin = [os.path.basename(sources[i]) in os.listdir(destination) for i in range(len(sources))]
        if True not in isin: #i.e. if none of the source files are in the destination folder
            print("Copying:", sources, "\n", "to:", destination)
            # copy all files in sources lists
            [call(["cp", "-a", "-R", i, destination]) for i in sources]
        else:
            #print([(os.path.basename(sources[i]) for i in range(len(sources)))])
            print('Not copying as source files in destination directory: {}'.format([os.path.basename(sources[i]) in os.listdir(destination) for i in range(len(sources))]))
        
            
