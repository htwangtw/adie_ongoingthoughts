'''
Gather subject IDs from a BIDS dataset

Usage:
python generate_participant.py
'''
from pathlib import Path
import os
import pandas as pd
#from adie.tests import get_test_data_path


#bids_dir = Path(get_test_data_path())
#subj = list(bids_dir.glob("sub-*"))

def generate_participants(bids_root):
    subj = list(bids_root.glob("sub-*")) # Lists directories
    sub_str = [str(e) for e in subj] # Subjects as string, converts elements from windows path to string retaining list format 

    sub_id = []
    while sub_str:  # stop when sub_str is empty
        cur_sub = sub_str.pop()  # pop an item from the list
        cur_sub = cur_sub.split(os.sep) # split string by os specific separator, return a list of strings
        sub_id.append(cur_sub[-1]) # save output

    #Convert list into a a dateframe
    df = pd.DataFrame(sub_id,columns=['participant_id'])
    df.to_csv(bids_root / 'participants.tsv', sep='\t', index=False) # Output to .tsv file
    
if __name__ == '__main__':
    project_root = Path(__file__).parents(2) 
    generate_participants(project_root)
