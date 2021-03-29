# Handling fMRI data

1. run_heudiconv.py: (i) get metadata for one participant and (ii) DICOM to BIDS for all participants.
2. csic_to_adie_conversion.py : change subject names from ADIE IDs to CISC IDs.
3. mirgrate_existing_subject.py : copy data to centralised BIDs dataset. Session names changed. 

# Understanding fMRI data

1. t1_and_mw_scan_descriptives.py : generate descriptive stats regaring subjects T1 and Mindwandering scans.
