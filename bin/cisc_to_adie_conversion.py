# Script to convert CISC ID to ADIE ID in directory and file names 
# This is only tested on directories/file£s with a BIDS naming convention
# The way the script searches for the sub- ID is dependent on the characters before and after,
# which is specific to BIDS - be aware  

import pandas as pd
import os 
import re
import shutil
import sys, os


# TODO: make this path relative to the user 

# TODO: Use something more forgiving than shutil.move? Maybe shutil.copy then delete the old dataset when 100% safe?
# shutil.move is quite desturctive in that it's deleting the old files
# and if something goes wrong halfway through a conversion, you're left with two incomplete datasets 

# TODO: Try this on edgy test cases as per H-T's previous comments (e.g. pytest)
# TODO: Figure out Github actions so i can get GH feedback on this script
# Refer to H-T's scripts for this 

#Import adie/cisc conversion txt file and store as dataframe
txt=("/Volumes/cisc2/projects/critchley_adie/BIDS_data/sourcedata/adie_idconvert.txt")

# convert this to dictonary, where key = CISC and val = ADIE 
rename = {}
with open(txt) as f:
    for line in f:
        (key,val)=line.split()
        #Remove any non-digit i.e. 'CISC'
        rename[str(re.sub("[^0-9]","",key))] = str(val)


# Function 1 - consolidate sub- dir as 'root' - bit redundent for now butmay come in handy 
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
        print("CISC ID not recognized!")

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

# -------------- RUN FUNCTIONS -------------- #

# For now, just loop over one subject for testing purposes 
path = '/Volumes/cisc2/projects/critchley_adie/wills_data/bids/bids_data2/sub-23014'

# Loop through each subject 
for sub in glob.glob(path):
    # F1 - List sub directory for searching  
    r = subpaths(sub)
    # F2 - Extract CISC ID from root name, and match with ADIE ID 
    newid,cid = idmatch(r)
    print(newid,cid)
    # F3 - Recreate directory sturcture, using new ID names
    newdir(newid,r)
    # F4 - Copy files from old to new structure, while renaming
    movefiles(sub,newid,cid)
