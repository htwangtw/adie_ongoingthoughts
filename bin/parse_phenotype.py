from pathlib import Path
import pandas as pd
import os
import json


# Create input/output variables
path = Path.cwd()
file = ("adie-questionnaires_patients.tsv")
df = os.path.join(path, file)
output_dir = (path / "patients_with_subid")

# Load .tsv file into dataframe
df = pd.read_csv(df, sep='\t')

# Denote session names for parsing assessment data
sessions = {
    "BL": "baseline",
    "F": "oneweek",  # confirmed by lisa
    "_3mf": "threemonth",
    "FY": "oneyear"
}


subid = "participant_id"
# curate session unrelated labels, pull column names from dataframe
demographics = ["participant_id", "Age", "GenderID", "GenderBirth", "GenderFit", "Education", "Handedness", "Nationality"]

height_weight = ["participant_id", "Height", "Weight"]

diagnosis = ["participant_id", "Medication", "PriorDx", "AnxietyDx", "DepressionDx",
    "ADHD", "OCD", "PTSD", "CPTSD", "Dyspraxia","Dyslexia", "EatingDisorder",
    "MINIDx", "MINIASCDx", "MINIYes"]

admin = ["participant_id", "Intervention", "Intero_Completion", "PrimOut", "Compliance", "Dropout", "Site"]

assessments = ["BPQ", "TAS", "AQ", "EQ", "STAI",
    "GAD7", "MAIA", "PANAS", "PHQ9", "UCLA", "GSQ"]  # known assessments

template = {"Descriptions": "fill this in",
            "Levels": {"item1": "description; delete if not applied",
                "item2": "description; delete if not applied"}
}
MeasurementToolMetadata = {
            "Description": "A free text description of the measurement tool",
            "TermURL": "A URL to an entity in an ontology corresponding to this tool"
            }

# Create separate files for session unrelated groups
for name, cat in zip(["demographics", "height_weight", "diagnosis", "admin"], # Variable 'name' string. Function 'zip' allows multiple column names into for loop
    [demographics, height_weight, diagnosis, admin]): # Variable 'cat' selects category
    # Create variable desc for .json file    
    desc = {c: template for c in cat} # [Column name: template] looped for column name in category (c = item in list)
    with open(output_dir / f"{name}.json", "w") as f: # Creates file based on f"{value}" ("w", truncates file) saves as 'f'
        json.dump(desc, f, indent=2) # Dumps desc variable into 'f'.json file 
    cur_df = df[cat].fillna("n/a").set_index("participant_id") # Fills blank cells in selected category of df with 'n/a'
    cur_df.to_csv(output_dir / f"{name}.tsv", sep="\t") # Saves category in .tsv file based on f'{name}' variable

for k in sessions: # Loops the session keys through the following function:
    def sess_parse(sess_key): # Funtion for extracting assessments based on session:
        for an in assessments: # 'an' = assessment name AKA for item in assessments list
            partid = [c for c in df.columns if subid in c]
            subscales = [c for c in df.columns if an in c]
            if sess_key == "F":
                sess_key = "F_"
                #subscales = [c for c in df.columns if an in c]  # Identifies columns containing 'an' AKA item in 'assessments'
                subscales = [c for c in subscales if sess_key in c] # Further identifies columns containing the session key 
                sess_key = "F"
                if subscales: # If subscales exist run this loop:
                    desc = {c.replace(sess_key, ""): template # Removes session indicator for .json file
                            for c in subscales if sess_key in c} # Only does the above for the following

                    desc["MeasurementToolMetadata"] = MeasurementToolMetadata # Adds 'measurementoolmetadata' to existing .json file
                    with open(output_dir / f"{an}_sess-{sess_key}.json", "w") as f: # Creates file based on f"{value}" ("w", truncates file) saves as 'f'
                        json.dump(desc, f, indent=2) # Dumps 'desc' variable into 'f'.json file 
                        cur_df = df[subscales].fillna("n/a") # Fills blank cells in selected columns off the dataframe with 'n/a'
                        partid = df[partid].fillna("n/a")
                        cur_df = cur_df.assign(participant_id=partid)
                        cur_df = cur_df.set_index("participant_id")
                        cur_df.to_csv(output_dir / f"{an}_sess-F.tsv", sep="\t") # Saves category in .tsv file based on f'{}' variables

            else:
                #subscales = [c for c in df.columns if an in c]  # Identifies columns containing 'an' AKA item in 'assessments'
                subscales = [c for c in subscales if sess_key in c] # Further identifies columns containing the session key 
                if subscales: # If subscales exist run this loop:
                    desc = {c.replace(sess_key, ""): template # Removes session indicator for .json file
                            for c in subscales if sess_key in c} # Only does the above for the following

                    desc["MeasurementToolMetadata"] = MeasurementToolMetadata # Adds 'measurementoolmetadata' to existing .json file
                    with open(output_dir / f"{an}_sess-{sess_key}.json", "w") as f: # Creates file based on f"{value}" ("w", truncates file) saves as 'f'
                        json.dump(desc, f, indent=2) # Dumps 'desc' variable into 'f'.json file 

                        cur_df = df[subscales].fillna("n/a") # Fills blank cells in selected columns off the dataframe with 'n/a'
                        partid = df[partid].fillna("n/a")
                        cur_df = cur_df.assign(participant_id=partid)
                        cur_df = cur_df.set_index("participant_id")
                        cur_df.to_csv(output_dir / f"{an}_sess-{sess_key}.tsv", sep="\t") # Saves category in .tsv file based on f'{}' variables
    sess_parse(k)
