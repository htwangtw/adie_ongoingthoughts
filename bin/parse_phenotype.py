from pathlib import Path
import pandas as pd
import os
import json
import re


# Create input/output variables
path = Path.cwd()
file = ("adie-questionnaires_patients.tsv")
df = os.path.join(path, file)
output_dir = (path / "test")

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

BL_one = ["participant_id", "BL_Track_meanacc", "BL_Track_RHO", "BL_Track_meanconf", "BL_Time_meanacc", "BL_Time_RHO",
       "BL_Time_meanconf", "BL_Disc_meanacc", "BL_Disc_ROC", "BL_Disc_meanconf", "BL_d_prime", "BL_ITPE_T", "BL_ITPE_D", BL_C]
F_one = ["participant_id", "F_Track_meanacc", "F_Track_RHO", "F_Track_meanconf", "F_Time_meanacc", "F_Time_RHO",
       "F_Time_meanconf", "F_Disc_meanacc", "F_Disc_ROC", "F_Disc_meanconf", "F_d_prime", "F_ITPE_T", "F_ITPE_D", F_C]

BL_assessment = ["participant_id", "BL_prosody_acc", "BL_face_acc", "BL_face_with_text_acc", "BL_text_acc", BL_percent_positive, BL_percent_negative,
       "BL_percent_positive_face", "BL_percent_negative_face", "BL_FaceAndext_Acc_Positive", "BL_FaceandText_Acc_Negative",
       "BL_Text_Acc_Positive", "BL_Text_Acc_Negative", "BL_Basic_emotions", "BL_complex_emotions",
       "BL_Basic_face_acc", "BL_complex_face_acc", "BL_basic_FaceAndText_Acc", "BL_Complex_FaceAndText_ACC", 
       "BL_basic_text_acc", "BL_complex_text_acc"]

F_assessment = ["participant_id", "F_prosody_acc_percent", "F_face_percent", "F_face_and_text_percent", "F_text_percent", 
       "F_positive_percent", "F_negative_percent","F_positive_face_percent", "F_negative_face_percent", "F_positive_face_and_text_percent", 
       "F_negative_face_and_text_percent","F_positive_text_percent", "F_negative_text_percent", "F_basic_emotions_percent",
       "F_complex_emotions_percent", "F_basic_face_percent", "F_complex_face_percent", "F_basic_face_and_text_percent", 
       "F_complex_face_and_text_percent", "F_basic_text", "F_complex_text"]


template = {"Descriptions": "fill this in",
            "Levels": {"item1": "description; delete if not applied",
                "item2": "description; delete if not applied"}
}
MeasurementToolMetadata = {
            "Description": "A free text description of the measurement tool",
            "TermURL": "A URL to an entity in an ontology corresponding to this tool"
            }

# Curate non-session related data and parse into separate .tsv & .json files
for name, cat in zip(["demographics", "height_weight", "diagnosis", "admin", "BL_assessment", "F_assessment", "one_ses-baseline", "one_ses-oneweek"], 
    [demographics, height_weight, diagnosis, admin, BL_assessment, F_assessment, BL_one, F_one]): 
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
            with open(output_dir / f"{an}_ses-{new_key}.json", "w") as f: 
                json.dump(desc, f, indent=2) 

