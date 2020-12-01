# script to enact the analysis plan 
# Aim is to take each particiapnts MW data and transpose into one data frame where there's one row per thought probe 

import glob
import os
import pandas as pd
import numpy as np

# this may change depending on who runs the script
base = '/Users/willstrawson/Documents/PhD/adie_ongoingthoughts/'

os.chdir(base)

# this should stay the same 
src = 'data/mw_data/mindwandering_data/*/*/*/*data.csv'
data = glob.glob(src)

# import each participants data as a dataframe (value) with their participant number & group as key 

dataframes = {}
for i in data:
    #extract participant number 
    subnum = i.split('/')[5]
    # extract group (control or ASC)
    group = i.split('/')[3]
    group = group.replace('_Participants','')
    # extract ECG group to either 'with_ECG' or 'without_ECG' 
    ecg = i.split('/')[4] 
    ecg = ecg.replace('Participants_','')
    ecg = ecg.replace('_data','')
    # import data as dataframe 
    dataframes[subnum,group,ecg] = pd.read_csv(i)


for i in dataframes:
    # remove whitespace and makecolumns lowercase 
    dataframes[i].columns = dataframes[i].columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace("'","")
    # keep only rows on which questions was being asked 
    # columns mwtype == TT or NT when no question being asked so drop based on this 
    dataframes[i] = dataframes[i].loc[dataframes[i]['mwtype'] != 'TT']
    dataframes[i] = dataframes[i].loc[dataframes[i]['mwtype'] != 'NT']

    # drop irrelivnt columns here - keep MW question label (mwtype), 0-back or 1-back label, and response
    dataframes[i] = dataframes[i][['nback','mwtype','keyresp']]
    # create column which indexes the question count number 
    dataframes[i]['q_count'] = None
     # create column which tracks which porbe numer
    dataframes[i]['probe_nr'] = None
    # create list to add questions labels to
    labels = []
    probe_counter = []
    # iterate row by row
    for u in dataframes[i].itertuples():
        # each time question asked, append label to list 
        labels.append(u.mwtype)
            # if the label has not already been added to list (1 count), probe == 1
            # probe number should = the number of times the label has appeared 
        dataframes[i].loc[u.Index, 'q_count'] = labels.count(u.mwtype)
        # add this label counter to the probe counter list 
        probe_counter.append(labels.count(u.mwtype))
        # probe number should = the max number of label count 
        dataframes[i].loc[u.Index, 'probe_nr'] = np.max(probe_counter)


# create new dict to store pivoted dataframes where one row = one probe 
dfs_perprobe = {}

for i in dataframes:
    # Rearange dataframe so that row = probe, columns = question 
    # omit values paramter to retain nback columns
    dfs_perprobe[i] = dataframes[i].pivot(index = 'probe_nr', columns = 'mwtype') # values = 'keyresp')
    # don't need qcount columns
    dfs_perprobe[i] = dfs_perprobe[i][['nback','keyresp']] 
    # This colummn contains all the info you needfor the nback column 
    dfs_perprobe[i]['n_back'] = dfs_perprobe[i]['nback','Deliberate']
    # Keep this newly created column and the key responses 
    dfs_perprobe[i] = dfs_perprobe[i][['keyresp','n_back']]   
    # remove level from column
    dfs_perprobe[i].columns = dfs_perprobe[i].columns.droplevel()
    # rename nback column due to droplevel removing the name 
    dfs_perprobe[i].rename(columns={'':'nback'}, inplace=True)
    # add  columns for dict keys 
    dfs_perprobe[i]['subnum'] = i[0]
    dfs_perprobe[i]['group'] = i[1]
    dfs_perprobe[i]['ecg'] = i[2]



# concatanate individual dataframes into one

df = pd.concat(dfs_perprobe, sort = True)

# make ecg column binary 
df.replace('with_ECG', '1', inplace = True)
df.replace('without_ECG', '0', inplace = True)

# save
df.to_csv('data/mw_data/processed_data/perprobe.csv', na_rep=np.nan, index=False)














