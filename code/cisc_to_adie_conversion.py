# Script to change directory names from CISC to AIDE ID 
import pandas as pd
import os 
import re

# TODO: make paths relative to each user of this script 

#Import adie/cisc conversion txt file and store as dataframe
txt="/Volumes/cisc2/projects/critchley_adie/BIDS_data/sourcedata/adie_idconvert.txt"
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
                        newf = f.replace(cidn,rename[cid])
                        print("Renaming",f,"to",newf)
                        os.rename(f,newf)
                        
                        # Replace f with newf
                    except Exception as e:
                        #print(e)
                        pass

            except Exception as e:
                    #print(e)
                    pass

        # Now repeat the process for Root directories
        try:
            # Search ID number after 'sub-' and before '/'
            srch = re.search('sub-(.+?)/',root)
            cidn = srch.group(1)
            cid = 'CISC'+str(cidn)
            if cid in rename.keys():
                try:
                # ... replace the CISC ID with ADIE ID 
                    newroot = root.replace(cidn,rename[cid])
                    print ("Renaming",root,"to",newroot)
                    os.rename(root,newroot)

                    # Replace f with newf
                except Exception as e:
                    print(e)
                    pass

        except Exception as e:
                print(e)
                pass

p = "/Volumes/cisc2/projects/critchley_adie/wills_data/bids/bids_data1/"

subconvert(p)




