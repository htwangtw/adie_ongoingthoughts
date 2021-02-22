"""
#!/usr/bin/env/ python 

Author: Will Strawson and Hao-Ting Wang, last updated 22-02-2021
Aim of this script is to convert CISC ID to ADIE ID in directory and file names 


Usage:
add how to use in the command line
"""

import pandas as pd
import os 
import re
import shutil
import sys, os
from pathlib import Path
import glob


# Script has to run from within critchely_adie/ cisc2 dir for the paths to work
# TODO: construct CISC2 file path
# TODO: change session- labels to be 'baseline' or 'intervention'


scriptpath = os.path.realpath(__file__)
print ('Script path =',scriptpath)
# Get path to ADIE dir - make it universal 
adie_dir = ('research/cisc2/projects/critchley_adie/')
#adie_dir = os.path.dirname(os.path.dirname(os.path.dirname(scriptpath)))
print('Main ADIE Directory =',adie_dir)
# import conversion txt file 
txtfile = os.path.join(adie_dir, 'BIDS_data/sourcedata/adie_idconvert.txt')
print ('Conversion txt file path =',txtfile)

# convert this to dictonary, where key = CISC and val = ADIE 
def convert_dict(txtfile):  
    rename = {}
    with open(txtfile) as f:
        for line in f:
            (key,val)=line.split()
            #Remove any non-digit i.e. 'CISC'
            rename[str(re.sub("[^0-9]","",key))] = str(val)
        return rename

# Function 1 - consolidate sub- dir as string - bit redundent for now but may come in handy 
def subpaths(sub):
    return str(sub)

# Function 2 - Extract CISC ID from directory, and match with ADIE ID 
def idmatch(r):
    # search for group of numbers after 'sub-'
    print(r)
    cid = re.search("sub-([0-9]*)",r).group(1)
    # match CISC ID with ADIE ID
    if cid in rename.keys():
        # return new ID with 'sub-' appended, as per BIDS convention, and CISCID
        return "sub-" + rename[cid], cid
    elif cid not in rename.keys():
        print("CISC ID ({}) not recognized!".format(cid))

# Function 3 - Create new directory with same structure 
def newdir(newid,root):
    # Recreat directory structure, using the parent sub- directory as input 
    for dirpath, dirnames, filenames in os.walk(r):
        structure = os.path.join(newid,os.path.relpath(dirpath,root))
        # Check to see if these new directories don't exist
        # if not, make the directory with the new ADIE names 
        if not os.path.isdir(structure):
            # need to change directory to the same level as existing sub- dir
            # to ensure to that new directory is not made inside the existing one
            parentdir = os.path.split(os.path.normpath(root))[0]
            os.chdir(parentdir)
            # create directory 
            os.makedirs(structure)
            print ("Creating {} inside {}".format(structure,os.getcwd()))
        else:
            print("Directory already exists!")

# Function 4 - Move files to new directories and rename 
def movefiles(sub,newid,cid):
    # construct full CISC ID (with sub-)
    cid_full = 'sub-'+cid
    for root,dirs,files in os.walk(sub):
        for f in files:
            # Only continue with the file if it's NOT a stupid annoying mac file
            if 'DS_Store' not in f:
                # Construct full path 
                fullf = os.path.join(root,f)
                # Create new path by replacing sub-CISCID with sub- ADIEID
                newf = fullf.replace(cid_full,newid)
                # Check that directories already exist - should've been created in F3 
                if not os.path.isdir(os.path.split(newf)[0]):
                    print("WARNING: '{}' does NOT exists".format(os.path.split(newf)[0]))
                # If directory does exist, proceed with move and rename    
                else:
                    print("Attempting to move",fullf,"to",newf,'\n')
                    shutil.move(fullf,newf)
            elif 'DS_Store' in f:
                continue

# Function 5 - Count number of files in a sub- dir 
def numfiles(subdr):
    # initialize variable
    numf = 0
    for root, dirs, files in os.walk(subdr):
        numf += len(files)
        return numf
    print ("Number of files in {}: {}".format(subdr,numf))

# Function 6 - remove redundent dirs
def compare(numf_old,numf_new,dir_to_del):
    if numf_old == numf_new:
        print ("Removing:",sub, '\n', 'Number of files equal - suggests successful conversion')
        shutil.rmtree(dir_to_del)
    else:
        print (" Not removing:",sub,'\n','Number of files not equal!')


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
txtfile = "/Volumes/cisc2/projects/critchley_adie/BIDS_data/sourcedata/adie_idconvert.txt"

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






