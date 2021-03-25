"""
Author: Will Strawson and Hao-Ting Wang 22-02-2021
Script to run heudiconv, once a heuristic file has been generated

Usage:
When running from command line, user can input the output directory.
Input is fixed to files within adie_dicoms/ and control_dicoms/ for now.
"""

import subprocess
import glob
import os

from pathlib import Path

repo_root = Path(__file__).parent

def subses(sub):
    """Explicitly define session names from directory names"""
    drs=glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/*'.format(sub))
    # save names of session level directories
    return [os.path.split(d)[1] for d in drs if 'DS_Store' not in d]


def run_heudiconv_func(sub,ses, out, getmetadata):  # sourcery skip: move-assign
    """ Run heudiconv with session flag, either to get metadata or to generate BIDS niftis"""
    # If working with new DICOMS in different directory, change this 'data' variable
    data = '/research/cisc2/projects/critchley_adie/*/CISC{subject}/{session}/*/*'
    # Let the user define this
    out = output_dir
    # If metadata already exists...
    if getmetadata == 'n':
        heuristic_path = str(repo_root / 'heudiconv/heuristic.py')
        print ('heuristic:',heuristic_path)
        for s in ses:
            print (len(glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))
            subprocess.call(['heudiconv','-d',data,'-f',heuristic_path,'-s',sub,'-ss',s,'-c','dcm2niix','-o',out, '-b','--overwrite'])
    # If metadata doesn't yet exist        
    elif getmetadata == 'y':
        
        for s in ses:
            print (len(glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))
            subprocess.call(['heudiconv','-d',data,'-f','convertall','-s',sub,'-ss',s,'-c','none','-o',out])
      

if __name__ == "__main__":
    ### Run functions ###
    # Get all subs
    output_dir = input("Please input the output directory path: \n")

    getmetadata = input("Do you need to get metadata first? (y/n)?")

    if getmetadata == 'n':
        subs = glob.glob('/research/cisc2/projects/critchley_adie/*_dicoms/CISC17875')
        #extract just sub name
        subs = [os.path.split(i)[1] for i in subs]
        subs = [i.replace('/','') for i in subs]
        subs = [i.replace('CISC','') for i in subs]

        print ("Number of subjects:",len(subs))
        print ("List of subjects:\n",subs)

    elif getmetadata == 'y':
        subs = glob.glob('/research/cisc2/projects/critchley_adie/*_dicoms/CISC*')
        subs = [os.path.basename(i) for i in subs]
        print('Available subjects:', subs)
        subs = input("Which subject would you like to use to generate metadata?\n Note: Only numbers from ID are needed (e.g. 1234 not CISC-1234):\n ")
    
    # convert string to one item in list so following for loop works
    if type(subs) == str:
        subs = [subs]
        print (subs, '\ntype:', type(subs))
    
    for idx,sub in enumerate(subs):
        ses = subses(sub)
        print(sub,'\n',ses)
        run_heudiconv_func(sub,ses, output_dir, getmetadata)
        print (idx+1,'/',len(subs))

