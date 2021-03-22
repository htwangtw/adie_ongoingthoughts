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

# Explicitly define sessionnames from directory names
# TODO: Change session nameto be 0,1,2
def subses(sub):
    drs=glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/*'.format(sub))
    ses = [os.path.split(d)[1] for d in drs if 'DS_Store' not in d]
    # save names of session level directories
    return ses

# Run heudiconv with session flag
def hc(sub,ses, out):
    data = '/research/cisc2/projects/critchley_adie/*/CISC{subject}/{session}/*/*'
    # Let the user define this
    out = output_dir
    heuristic_path = str(repo_root / 'heuristic/heuristic.py')

    for s in ses:
        print (len(glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))

        subprocess.call(['heudiconv','-d',data,'-f',heuristic_path,'-s',sub,'-ss',s,'-c','dcm2niix','-o',out, '-b','--overwrite'])


if __name__ == "__main__":
    ### Run functions ###
    # Get all subs
    output_dir = input("Please input the output directory path: \n")

    subs = glob.glob('/research/cisc2/projects/critchley_adie/*_dicoms/CISC*')

    #extract just sub name
    subs = [os.path.split(i)[1] for i in subs]
    subs = [i.replace('/','') for i in subs]
    subs = [i.replace('CISC','') for i in subs]

    print ("Number of subjects:",len(subs))
    print ("List of subjects:\n",subs)

    for idx,sub in enumerate(subs):
        ses = subses(sub)
        print(sub,'\n',ses)
        hc(sub,ses, output_dir)
        print (idx,'/',len(subs))

