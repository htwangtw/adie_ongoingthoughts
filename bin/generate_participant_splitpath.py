from pathlib import Path
import os
import pandas as pd


data = Path.cwd()
subj = list(data.glob("Sub_*")) # Lists directories
sub_str = [str(e) for e in subj] # Subjects as string, converts elements from windows path to string retaining list format 
total_elements = len(sub_str) # Variable for while loop
element = 0 # List elements start at 0

while element <= total_elements - 1: # Total_elements = 4 in this instance

    headtail = os.path.split(sub_str[element])
    sub_str[element] = headtail[1]
    
    element = element + 1 #End of loop

#Convert list into a a dateframe
df = pd.DataFrame(sub_str,columns=['Subjects'])
print (df)

df.to_csv('Participant_generator.tsv', sep='\t', index=False) # Output to .tsv file
