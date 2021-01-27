# Script to run heudiconv (no heuristic)

import subprocess
import glob
import os

# Explicitly define sessionnames from directory names
def subses(sub):
    drs=glob.glob('/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{}/*'.format(sub))
    ses = [os.path.split(d)[1] for d in drs if 'DS_Store' not in d]
    # save names of session level directories 
    return ses

# Run heudiconv with session flag
def hc(sub,ses):
    out = '/its/home/ws231/Desktop/cisc2/projects/critchley_adie/wills_data'
    pth = '/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{subject}/{session}/*/*'
    for s in ses:
        print (len(glob.glob('/its/home/ws231/Desktop/cisc2/projects/critchley_adie/*/CISC{}/{}/*/*'.format(sub,s))))

        subprocess.call(['heudiconv','-d',pth,'-f','convertall','-s',sub,'-ss',s,'-c','none','-o',out])

sub = '7426'

ses = subses(sub)
print(sub,'\n',ses)
hc(sub,ses)
