# Analysis Plan 

## Aim: To understand patterns of ongoing thought in the ASD patients and controls during n-back task. 

### The data will come from thought probes during n-back task.

---

1. Locate raw data 

   - One row per question 

2. Gather all such data, adding a column for whether they were a) control/ASC ; b) with/without ECG ; participant number 

3. Transpose data so that one row = one thought probe 

   - Will have multiiple rows per participant 

4. Run PCA 

   a) Run one PCA on all data

   b) Supplementary: Run seperate PCAs for each group & sub group, and see how the extracted componants correlate with the original main factors. 

5. How do the factor loadings differ as a function of group (asc vs controls) and trial (0-back 1-back)

   - LMM in R 
   - Fixed effects: Trial type (0-back/1-back), Group (Control or ASD)
   - Use pca_res.csv, from pca.py script 

## 



