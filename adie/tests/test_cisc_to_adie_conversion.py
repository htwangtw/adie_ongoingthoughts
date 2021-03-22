from pathlib import Path

# Import functions i wrote 
from adie.cisc_to_adie_conversion import *
# from utils 
from adie.tests import get_test_data_path

print (Path(get_test_data_path))

# Loop through each subject 
def test_convervion(subs):
    for sub in glob.glob(subs):
        # F1 - List sub directory for searching  
        r = subpaths(sub)
        # F2 - Extract CISC ID from root name, and match with ADIE ID 
        newid,cid = idmatch(r)
        print(newid,cid)
        # F3 - Recreate directory sturcture, using new ID names
        newdir(newid,r)
        # F4 - Copy files from old to new structure, while renaming
        movefiles(sub,newid,cid)

subs = 





