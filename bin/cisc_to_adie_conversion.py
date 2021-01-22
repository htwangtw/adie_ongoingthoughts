# Script to convert CISC ID to ADIE ID in directory and file names 
# This is only tested on directories/file£s with a BIDS naming convention
# The way the script searches for the sub- ID is dependent on the characters before and after,
# which is specific to BIDS - be aware  

import pandas as pd
import os 
import re
import shutil
import sys, os

'''
# Construct path of converter .txt file such that it's relative to the user running the script
# Get parent directory of this script       
pathname = os.path.dirname(sys.argv[0])  
# Get the level above that (i.e. the critchley_adie project dir)      
project_path = os.path.split(pathname)[0]
print('project_path=',project_path)
'''

#TODO: make this path relative to the user 
#Import adie/cisc conversion txt file and store as dataframe
txt=("/Volumes/cisc2/projects/critchley_adie/BIDS_data/sourcedata/adie_idconvert.txt")

# convert this to dictonary, where key = CISC and val = ADIE 
rename = {}
with open(txt) as f:
    for line in f:
        (key,val)=line.split()
        rename[str(key)] = str(val)


# USE OS.WALK

def subconvert(p):
# P should = the path of the directory above the sub- dirs 
    for root,dirs,files in os.walk(p):
        for f in files:
            # Extract sub- number for searching 
            # Extract number after 'sub-' and before '_'
            try:
                srch = re.search('sub-(.+?)_',f)
                # extract just ID number
                cidn = srch.group(1)
                # Add CISC to ID to enable search 
                cid = 'CISC'+str(cidn)
                # If this file contrains the CISC ID...
                
                if cid in rename.keys():
                    #print (cid,rename[cid])
                    try:
                        # ... replace the CISC ID with ADIE ID 
                        # add root to filename and then replace 
                        fullf = os.path.join(root,f)
                        newf = fullf.replace(cidn,rename[cid])
                        print("Renaming",fullf,"to",newf)

                        # Rename file and directory 
                        # !! getting "no such file found" error 
                        # I'm to create new file name and  directory name that doesn't yet exist...
                        # TODO: figure a way of renaming both levels at the same time OR create directory first 
                        shutil.move(os.path.join(root,f), os.path.join(root,newf))
                        
                    # If error occured with .replace or .move, print error
                    except Exception as e:
                        print(e)
                        
            # If error occured with re.search, print error 
            except Exception as e:
                    print(e)

            print('\n')
        print('-'*100)   

#test path
path = "/Volumes/cisc2/projects/critchley_adie/wills_data/bids/bids_data2/sub-23014/"

subconvert(path)




