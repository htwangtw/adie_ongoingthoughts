from pathlib import Path
Path.cwd()
data = Path.cwd()
data.absolute() # Prints absolute path
data.glob("Sub_01") # Selects all directories named Sub_* In Python, the glob module is used to retrieve files/pathnames matching a specified pattern.
subj=list(data.glob("Sub_01")) # Lists directories

sub_str = [ str(e) for e in subj] # subjects as string, converts elements from windows path to string retaining list format

import os  
len(sub_str) # Equals amount of elements in substr list
total_elements = len(sub_str) # Variable for while loop
element = 0 # List elements start at 0

while element <= total_elements-1: # total_elements = 4 in this instance

    headtail = os.path.split(sub_str[element])
    sub_str[element] = headtail[1]
    
    element = element+1 #End of loop

#Convert list into a a dateframe
from pandas import DataFrame
df = DataFrame (sub_str,columns=['Subjects'])
print (df)

df.to_csv('Participant_generator.tsv', sep = '\t', index=False) # Output to .tsv file