# Analysis Plan 

## Aim: To understand patterns of ongoing thought in the ASD patients and controls during n-back task. 

### The data will come from thought probes during n-back task.

---

1. Locate raw data 

   - One row per question 

2. Gather all such data, adding a column for whether they were a) control/ASD ; b) with/without ECG c) participant number d) RCT - interoceptive or exteroceptive task 

3. Transpose data so that one row = one thought probe (Will have multiiple rows per participant) 

4. Run PCA 

   - Run one PCA on all data

   - Supplementary: Run seperate PCAs for each group & sub group, and see how the extracted componants correlate with the original main factors. 

5. Present the data from this PCA in the form of wordclouds and heatmaps 

6. TODO: Linear mixed Model 

   - How do the factor loadings differ as a function of group (asc vs controls), trial (0-back 1-back) and timepoint (baseline vs post training)?

   - Fixed effects: Trial type (0-back/1-back), Group (Control or ASD), timepoint (baseline or posttraining)
   - Use pca_res.csv, from pca.py script 

## 



