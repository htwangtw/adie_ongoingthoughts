# Script to run heudiconv (with heuristic)

import subprocess
import glob
import os

# Explicitly define sessionnames from directory names
# TODO: Change session nameto be 0,1,2
def subses(sub):
    drs=glob.glob('/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{}/*'.format(sub))
    # save names of session level directories
    return [os.path.split(d)[1] for d in drs if 'DS_Store' not in d]

# Run heudiconv with session flag
def hc(sub,ses):
    data = '/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{subject}/{session}/*/*'
    out = '/its/home/ws231/Desktop/cisc2/projects/critchley_adie/wills_data/bids'
    heuristic_path ='/its/home/ws231/Desktop/cisc2/projects/critchley_adie/wills_data/code/heuristic.py'

    for s in ses:
        print (len(glob.glob('/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))

        subprocess.call(['heudiconv','-d',data,'-f',heuristic_path,'-s',sub,'-ss',s,'-c','dcm2niix','-o',out, '-b','--overwrite'])

# Run functions 
# Get all subs 
subs = glob.glob('/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*_dicoms/CISC*')
#extract just sub name 
subs = [os.path.split(i)[1] for i in subs]
subs = [i.replace('/','') for i in subs]
subs = [i.replace('CISC','') for i in subs]

print ("Number of subjects:",len(subs))
print (subs)

for idx,sub in enumerate(subs):
    ses = subses(sub)
    print(sub,'\n',ses)
    hc(sub,ses)
    print (idx,'/',len(subs))

