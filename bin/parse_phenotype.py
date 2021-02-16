from pathlib import Path
import pandas as pd
import os
import json
import re

# Create input/output variables
path = Path.cwd()
file = ("adie-questionnaires_patients.tsv")
df = os.path.join(path, file)
output_dir = (path / "results")

# Load .tsv file into dataframe
df = pd.read_csv(df, sep='\t')

# Denote session names for parsing assessment data
sessions = {
    "BL_": "baseline",
    "F_": "oneweek", 
    "_3mf": "threemonth",
    "FY": "oneyear"
}

# curate session unrelated labels, pull column names from dataframe
subid = "participant_id"

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

# Curate non-session related data and parse into separate .tsv & .json files
for name, cat in zip(["demographics", "height_weight", "diagnosis", "admin"], 
    [demographics, height_weight, diagnosis, admin]): 
    desc = {c: template for c in cat} 
    with open(output_dir / f"{name}.json", "w") as f: 
        json.dump(desc, f, indent=2) 
    cur_df = df[cat].fillna("n/a").set_index("participant_id") 
    cur_df.to_csv(output_dir / f"{name}.tsv", sep="\t") 

# curate session related data and parse into separate .tsv & .json files
for old_key, new_key in sessions.items(): 
    for an in assessments: 
        partid = [c for c in df.columns if subid in c]
        subscales = [c for c in df.columns if an in c] 
        subscales = [c for c in subscales if old_key in c] 
        if subscales:    
            cur_df = df[subscales].fillna("n/a") 
            partid = df[partid].fillna("n/a")
            cur_df = cur_df.assign(participant_id=partid)
            cur_df = cur_df.set_index("participant_id")
            cur_df.columns = [re.sub(old_key, '', col) for col in cur_df]
            cur_df.to_csv(output_dir / f"{an}_sess-{new_key}.tsv", sep="\t") 

            desc = {c.replace(old_key, ""): template 
                    for c in subscales if old_key in c}
            desc["MeasurementToolMetadata"] = MeasurementToolMetadata
            with open(output_dir / f"{an}_sess-{new_key}.json", "w") as f: 
                json.dump(desc, f, indent=2) 

