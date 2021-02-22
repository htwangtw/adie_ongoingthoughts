"""
Author: Will Strawson and Hao-Ting Wang 22-02-2021
Script to generate the metadata (heuristic.py) file needed for heudiconv to run

Usage:
User can input the subject ID which they'd like to run this on.

"""



import subprocess
import glob
import os

# Explicitly define sessionnames from directory names
def subses(sub):
    drs=glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/*'.format(sub))
    ses = [os.path.split(d)[1] for d in drs if 'DS_Store' not in d]
    # save names of session level directories 
    return ses

# Run heudiconv with session flag
def hc(sub,ses, out):
    out = output_dir
    pth = '/research/cisc2/projects/critchley_adie/*/CISC{subject}/{session}/*/*'
    for s in ses:
        print (len(glob.glob('/research/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))

        subprocess.call(['heudiconv','-d',pth,'-f','convertall','-s',sub,'-ss',s,'-c','none','-o',out])

### Run functions ###
available_subs = print(glob.glob('/research/cisc2/projects/critchley_adie/*_dicoms/CISC*'))
available=input("Would you like to see available subjects on which metadata can be generated from? [y/n]")

if available == 'y':
    print (available_subs)

sub = input("Which subject would you like to use to generate metadata?\n Note: Only numbers from ID are needed (e.g. 1234 not CISC-1234")

output_dir = input("Please input the output directory path: \n")

ses = subses(sub)
print('subject='sub,'\n','session=',ses)
hc(sub,ses, output_dir)
